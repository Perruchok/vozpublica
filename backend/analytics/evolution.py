# Time series semantics 
import numpy as np
from collections import defaultdict
from app import get_pool

async def fetch_relevant_embeddings(
    concept_embedding: list[float],
    similarity_threshold: float = 0.75
):
    pool = await get_pool()

    sql = """
    SELECT
      date_trunc('month', published_at) AS period,
      embedding
    FROM speech_turns
    WHERE
      published_at IS NOT NULL
      AND 1 - (embedding <=> $1::vector) > $2
    ORDER BY period;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, concept_embedding, similarity_threshold)

    return rows

def group_by_period(rows):
    buckets = defaultdict(list)

    for row in rows:
        period = row["period"]
        embedding = np.array(row["embedding"])
        buckets[period].append(embedding)

    return buckets
