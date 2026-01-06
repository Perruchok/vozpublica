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
      doc_id,
      sequence,
      speaker_raw,
      text,
      1 - (embedding <=> $1::vector) AS similarity
    FROM speech_turns
    ORDER BY embedding <=> $1::vector
    LIMIT $2;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, top_k)

    if not rows:
        return None

    # 3️⃣ Build context for RAG
    context = "\n\n".join(
        f"[{r['doc_id']} | {r['speaker_raw']}]\n{r['text']}"
        for r in rows
    )

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
                    "Cite the source when relevant."
                    #"If provided context is enough, provide detailed answer."

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
        # TODO: consider adding these parameters later
        # top_p=1.0,
        # frequency_penalty=0.0,
        # presence_penalty=0.0
    )

    answer = response.choices[0].message.content

    return answer, rows
