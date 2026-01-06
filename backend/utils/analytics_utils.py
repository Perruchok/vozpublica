"""
Analytics utilities for semantic drift analysis and narrative evolution.
"""
import os
import asyncpg
import numpy as np
import json
from collections import defaultdict
from scipy.spatial.distance import cosine
from openai import AzureOpenAI
from typing import List, Dict, Tuple
from datetime import datetime


# Database connection
pool = None

async def get_pool():
    """Get or create database connection pool."""
    global pool
    if pool is None:
        pg_host = os.environ["PGHOST"]
        pg_user = os.environ["PGUSER"]
        pg_password = os.environ["PGPASSWORD"]
        pg_db = os.environ["PGDATABASE"]
        pg_port = os.environ.get("PGPORT", "5432")
        DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}?sslmode=require"
        
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
    return pool


async def fetch_relevant_embeddings(
    concept_embedding: List[float],
    similarity_threshold: float = 0.6
):
    """
    Fetch speech turn embeddings that are similar to the concept embedding.
    
    Args:
        concept_embedding: The embedding vector for the concept
        similarity_threshold: Minimum similarity score (0-1)
    
    Returns:
        List of database rows with period and embedding data
    """
    pool = await get_pool()
    
    # Convert embedding to pgvector format
    embedding_str = '[' + ','.join(map(str, concept_embedding)) + ']'

    sql = """
    SELECT
      date_trunc('month', m.published_at) AS period,
      s.embedding
    FROM speech_turns s
    JOIN raw_transcripts_meta m
      ON s.doc_id = m.doc_id
    WHERE
      m.published_at IS NOT NULL
      AND 1 - (s.embedding <=> $1::vector) > $2
    ORDER BY period;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, similarity_threshold)

    return rows


async def fetch_sentences(
    concept_embedding: List[float],
    date_range: Tuple[str, str],
    similarity_threshold: float = 0.6
):
    """
    Fetch individual sentences within a date range that match the concept.
    
    Args:
        concept_embedding: The embedding vector for the concept
        date_range: Tuple of (start_date, end_date) in "YYYY-MM-DD" format
        similarity_threshold: Minimum similarity score (0-1)
    
    Returns:
        List of database rows with sentence data
    """
    pool = await get_pool()
    
    # Convert embedding to pgvector format
    embedding_str = '[' + ','.join(map(str, concept_embedding)) + ']'
    
    # Convert date strings to datetime objects
    start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
    end_date = datetime.strptime(date_range[1], "%Y-%m-%d")

    sql = """
        SELECT
        s.speaker_raw,
        s.speaker_normalized,
        s.embedding,
        s.text,
        m.published_at,
        1 - (s.embedding <=> $1::vector) AS similarity
        FROM speech_turns s
        JOIN raw_transcripts_meta m
        ON s.doc_id = m.doc_id
        WHERE
        m.published_at BETWEEN $2 AND $3
        AND s.embedding IS NOT NULL
        AND s.speaker_raw IS NOT NULL
        AND length(s.text) > 100
        AND 1 - (s.embedding <=> $1::vector) > $4
        ORDER BY similarity DESC
        LIMIT 200;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            sql,
            embedding_str,
            start_date,
            end_date,
            similarity_threshold
        )
    return rows


def group_by_period(rows):
    """
    Group embeddings by time period.
    
    Args:
        rows: Database rows with 'period' and 'embedding' fields
    
    Returns:
        Dictionary mapping periods to lists of embedding vectors
    """
    buckets = defaultdict(list)

    for row in rows:
        period = row["period"]
        # Convert embedding from string to numpy array
        embedding_str = row["embedding"]
        if isinstance(embedding_str, str):
            embedding = np.array(json.loads(embedding_str))
        else:
            embedding = np.array(embedding_str)
        buckets[period].append(embedding)

    return buckets


def group_embeddings_by_speaker(rows):
    """
    Group embeddings by speaker.
    
    Args:
        rows: Database rows with speaker and embedding fields
    
    Returns:
        Dictionary mapping speakers to lists of embedding vectors
    """
    buckets = defaultdict(list)

    for r in rows:
        speaker = r.get("speaker_normalized") or r.get("speaker_raw")

        # Skip rows with no speaker
        if not speaker:
            continue

        embedding_data = r["embedding"]
        if isinstance(embedding_data, str):
            embedding = np.array(json.loads(embedding_data))
        else:
            embedding = np.array(embedding_data)

        buckets[speaker].append(embedding)

    return buckets


def average_embedding(embeddings: List[np.ndarray]) -> np.ndarray:
    """Average multiple embedding vectors."""
    return np.mean(embeddings, axis=0)


def average_embeddings(grouped: Dict, min_evidence: int = 2) -> Dict:
    """
    Average embeddings for each group with minimum evidence threshold.
    
    Args:
        grouped: Dictionary mapping keys to lists of embeddings
        min_evidence: Minimum number of embeddings required
    
    Returns:
        Dictionary mapping keys to averaged embeddings
    """
    return {
        key: np.mean(vectors, axis=0)
        for key, vectors in grouped.items()
        if len(vectors) >= min_evidence
    }


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine distance between two vectors."""
    return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def semantic_drift(period_embeddings: Dict) -> List[Dict]:
    """
    Calculate semantic drift between consecutive time periods.
    
    Args:
        period_embeddings: Dictionary mapping periods to embedding vectors
    
    Returns:
        List of dictionaries with drift measurements between periods
    """
    periods = sorted(period_embeddings.keys())
    drift = []

    for i in range(1, len(periods)):
        t_prev = periods[i - 1]
        t_curr = periods[i]

        dist = cosine_distance(
            period_embeddings[t_prev],
            period_embeddings[t_curr]
        )

        drift.append({
            "from": t_prev,
            "to": t_curr,
            "semantic_change": float(dist)
        })

    return drift


def speaker_drift(pre_avg: Dict, post_avg: Dict) -> Dict:
    """
    Calculate semantic drift for each speaker between two periods.
    
    Args:
        pre_avg: Dictionary of averaged embeddings for pre-period
        post_avg: Dictionary of averaged embeddings for post-period
    
    Returns:
        Dictionary mapping speakers to their drift scores, sorted by drift
    """
    drift = {}
    for speaker in pre_avg:
        if speaker in post_avg:
            drift[speaker] = cosine(pre_avg[speaker], post_avg[speaker])
    return dict(sorted(drift.items(), key=lambda x: x[1], reverse=True))


def top_sentences(rows, n: int = 10) -> List[Dict]:
    """
    Extract top N sentences with their metadata.
    
    Args:
        rows: Database rows with sentence data
        n: Number of top sentences to return
    
    Returns:
        List of dictionaries with sentence metadata
    """
    return [
        {
            "speaker": r["speaker_normalized"],
            "date": r["published_at"],
            "text": r["text"],
            "similarity": r["similarity"]
        }
        for r in rows[:n]
    ]


def format_excerpts(sentences: List[Dict], max_items: int = 10) -> str:
    """
    Format sentences into a text block for LLM analysis.
    
    Args:
        sentences: List of sentence dictionaries
        max_items: Maximum number of sentences to include
    
    Returns:
        Formatted string with excerpts
    """
    lines = []
    for s in sentences[:max_items]:
        line = (
            f"- ({s['date'].date()}) "
            f"[{s['speaker']}] "
            f"{s['text'].strip()}"
        )
        lines.append(line)

    return "\n".join(lines)


def explain_semantic_drift(
    concept: str,
    drift_score: float,
    pre_sentences: List[Dict],
    post_sentences: List[Dict],
    model: str = "gpt-4.1"
) -> str:
    """
    Use an LLM to interpret semantic drift between two time periods.
    
    Args:
        concept: The concept being analyzed
        drift_score: Measured drift score
        pre_sentences: Sentences from the pre-period
        post_sentences: Sentences from the post-period
        model: Azure OpenAI model deployment name
    
    Returns:
        LLM-generated explanation of the semantic drift
    """
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

    pre_block = format_excerpts(pre_sentences)
    post_block = format_excerpts(post_sentences)

    system_prompt = (
        "You are a discourse analyst assisting with semantic analysis.\n"
        "You MUST rely ONLY on the provided excerpts.\n"
        "Do NOT speculate beyond the text.\n"
        "Cite specific phrases or patterns when making claims."
    )

    user_prompt = f"""
We measured a semantic drift score of approximately {drift_score:.2f}
for the concept "{concept}" between two time periods.

TASK:
1. Compare how the concept is framed in each period.
2. Identify changes in emphasis, scope, or framing.
3. Point to concrete textual evidence.
4. Explain how these differences plausibly account for the measured drift.

PRE-PERIOD EXCERPTS:
{pre_block}

POST-PERIOD EXCERPTS:
{post_block}

Respond using the following structure:

- Core framing (pre vs post)
- Concepts that gained prominence
- Concepts that lost prominence
- Overall semantic shift (grounded in text)
"""

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_completion_tokens=2000
    )

    return response.choices[0].message.content


def save_analysis(
    concept: str,
    explanation: str,
    pre_range: Tuple[str, str],
    post_range: Tuple[str, str],
    output_dir: str = "."
) -> str:
    """
    Save semantic drift analysis to a text file.
    
    Args:
        concept: The concept being analyzed
        explanation: LLM-generated explanation
        pre_range: Pre-period date range
        post_range: Post-period date range
        output_dir: Directory to save the file
    
    Returns:
        Path to the saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_drift_analysis_{concept.replace(' ', '_')}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Semantic Drift Analysis\n")
        f.write(f"Concept: {concept}\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Pre-period: {pre_range[0]} to {pre_range[1]}\n")
        f.write(f"Post-period: {post_range[0]} to {post_range[1]}\n")
        f.write(f"\n{'='*80}\n\n")
        f.write(explanation)

    return filepath
