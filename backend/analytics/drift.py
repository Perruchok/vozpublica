"""
Functions for analyzing semantic drift between specific time periods.
Used primarily for explaining drift with LLM context.
"""
import os
import numpy as np
import json
from datetime import datetime
from scipy.spatial.distance import cosine
from openai import AzureOpenAI
from backend.utils.dbpool import get_pool


async def fetch_sentences(
    concept_embedding: list[float],
    date_range: tuple[str, str],
    similarity_threshold: float = 0.6,
    top_k: int = 100
):
    """Fetch relevant sentences for a concept in a given date range."""
    pool = await get_pool()
    
    # Convert embedding to pgvector format
    embedding_str = '[' + ','.join(map(str, concept_embedding)) + ']'
    
    # Convert date strings to datetime objects
    start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
    end_date = datetime.strptime(date_range[1], "%Y-%m-%d")

    sql = """
        SELECT
            s.doc_id,
            s.speaker_raw,
            s.speaker_normalized,
            s.embedding,
            s.text,
            m.published_at,
            m.href,
            1 - (s.embedding <=> $1::vector) AS similarity
        FROM speech_turns s
        JOIN raw_transcripts_meta m
            ON s.doc_id = m.doc_id
        WHERE
            m.published_at BETWEEN $2 AND $3
            AND s.embedding IS NOT NULL
            AND 1 - (s.embedding <=> $1::vector) > $4
        ORDER BY similarity DESC
        LIMIT $5;
    """
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            sql,
            embedding_str,
            start_date,
            end_date,
            similarity_threshold,
            top_k
        )
    return rows


def top_sentences(rows, n=10):
    """Extract top N sentences from query results."""
    return [
        {
            "doc_id": r["doc_id"],
            "speaker": r["speaker_normalized"] or r["speaker_raw"],
            "date": r["published_at"],
            "text": r["text"],
            "similarity": float(r["similarity"]),
            "href": r["href"]
        }
        for r in rows[:n]
    ]


def average_embedding(embeddings: list[np.ndarray]) -> np.ndarray:
    """Compute the average of a list of embeddings."""
    return np.mean(embeddings, axis=0)


def calculate_semantic_change(pre_embeddings: list, post_embeddings: list) -> float:
    """Calculate semantic change between two periods using cosine distance."""
    pre_avg = average_embedding([np.array(e) for e in pre_embeddings])
    post_avg = average_embedding([np.array(e) for e in post_embeddings])
    
    return float(cosine(pre_avg, post_avg))


def format_excerpts(sentences, max_items=10):
    """Format top sentences into a controlled text block for the LLM."""
    lines = []
    for s in sentences[:max_items]:
        # Format with markdown link reference: [doc_id](href)
        ref = f"[{s['doc_id']}]({s['href']})" if s.get('href') else s['doc_id']
        line = (
            f"- ({s['date'].date()}) "
            f"[{s['speaker']}] "
            f"{s['text'].strip()} "
            f"(Ref: {ref})"
        )
        lines.append(line)
    
    return "\n".join(lines)


def explain_semantic_drift_with_llm(
    concept: str,
    drift_score: float,
    pre_sentences: list[dict],
    post_sentences: list[dict]
) -> dict:
    """
    Use an LLM to interpret semantic drift between two time periods.
    Returns structured JSON with summary, drivers, and contrasting examples.
    """
    
    pre_block = format_excerpts(pre_sentences)
    post_block = format_excerpts(post_sentences)

    system_prompt = (
        "You are a discourse analyst assisting with semantic analysis.\n"
        "You MUST rely ONLY on the provided excerpts.\n"
        "Do NOT speculate beyond the text.\n"
        "Cite specific phrases or patterns when making claims.\n"
        "IMPORTANT: Respond in SPANISH unless the concept being analyzed is in English.\n"
        "Respond in JSON format."
    )

    user_prompt = f"""
We measured a semantic drift score of {drift_score:.2f} for the concept "{concept}" between two time periods.

TASK:
1. Compare how the concept is framed in each period.
2. Identify changes in emphasis, scope, or framing.
3. Point to concrete textual evidence.
4. Explain how these differences plausibly account for the measured drift.
5. When citing excerpts, include the reference links provided (Ref: [doc_id](url)) to support your claims.

FIRST PERIOD EXCERPTS:
{pre_block}

SECOND PERIOD EXCERPTS:
{post_block}

Respond with a JSON object with exactly these keys:
{{
  "core_framing": {{
    "first_period": "description with citations [doc_id](url)",
    "second_period": "description with citations [doc_id](url)"
  }},
  "gained_prominence": ["concept 1", "concept 2"],
  "lost_prominence": ["concept 1", "concept 2"],
  "overall_shift": "explanation with citations [doc_id](url)"
}}

IMPORTANT: 
- Use exact key names: core_framing, gained_prominence, lost_prominence, overall_shift
- Include reference links in markdown format: [doc_id](url) 
- Keep text concise but grounded in evidence
"""

    # Get Azure OpenAI settings from environment
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    azure_openai_chat_deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4.1")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version
    )

    response = client.chat.completions.create(
        model=azure_openai_chat_deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_completion_tokens=1000,
        response_format={"type": "json_object"}
    )

    # Parse JSON response
    import json
    result = json.loads(response.choices[0].message.content)
    
    return result
