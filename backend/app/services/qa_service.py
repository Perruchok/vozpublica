from backend.utils.dbpool import get_pool
from backend.utils.postprocessing_helpers import embed_text
from openai import AzureOpenAI

from backend.settings import (
    azure_openai_endpoint,
    azure_openai_api_key,
    azure_openai_api_version,
    azure_openai_chat_deployment
)

async def answer_question(question: str, top_k: int):
    """
    Answers a question using a retrieval-augmented generation approach.
    Args:
        question (str): The question to answer.
        top_k (int): The number of top relevant documents to retrieve.
    Returns:
        answer (str): The generated answer.
        sources (list): List of source documents used for the answer.
    """
    # 1️⃣ Embed question
    embedding = embed_text(question)
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'

    # 2️⃣ Vector search
    pool = await get_pool()

    sql = """
    SELECT
      st.doc_id,
      st.sequence,
      st.speaker_raw,
      st.text,
      rtm.title,
      rtm.href,
      1 - (st.embedding <=> $1::vector) AS similarity
    FROM speech_turns st
    LEFT JOIN raw_transcripts_meta rtm ON st.doc_id = rtm.doc_id
    ORDER BY st.embedding <=> $1::vector
    LIMIT $2;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, top_k)

    if not rows:
        return None

    # 3️⃣ Build context for RAG with markdown links
    context_lines = []
    for i, r in enumerate(rows, 1):
        # Format with markdown link reference: [doc_id](href)
        ref = f"[{r['doc_id']}]({r['href']})" if r.get('href') else r['doc_id']
        context_lines.append(
            f"[Ref {i}: {ref}]\n"
            f"[{r['speaker_raw']}]\n"
            f"{r['text']}"
        )
    context = "\n\n".join(context_lines)

    # 4️⃣ Call LLM
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version
    )

    response = client.chat.completions.create(
        model=azure_openai_chat_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that answers questions using ONLY the provided context. "
                    "If the answer is not contained in the context, say you don't know. "
                    "IMPORTANT: When citing information, include the reference links in markdown format: [Ref 1](url). "
                    "This allows readers to verify the sources. "
                    "Example: 'Según la presidenta [Ref 1](https://example.com/doc1), la política de seguridad...'\n\n"
                    "CRITICAL: Respond in the same language as the user's question. "
                    "If asked in Spanish, respond only in Spanish. "
                    "If asked in English, respond only in English."
                )
            },
            {
                "role": "system",
                "content": f"Context:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=600,
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return answer, rows

