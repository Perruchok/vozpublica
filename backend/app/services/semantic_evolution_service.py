import numpy as np
from collections import defaultdict
from datetime import date
from backend.utils.dbpool import get_pool
from backend.utils.postprocessing_helpers import embed_text
from backend.analytics.narrative_evolution import (
    group_embeddings_by_period,
    compute_centroids,
    compute_evolution_points,
    compute_drift
)


async def compute_semantic_evolution(
    concept: str,
    granularity: str,
    start_date: date,
    end_date: date,
    similarity_threshold: float
):
    """
    Compute semantic evolution metrics for a concept over time.
    
    Args:
        concept: The concept to analyze
        granularity: Time granularity ('month', 'week', 'day')
        start_date: Start date for analysis
        end_date: End date for analysis
        similarity_threshold: Minimum similarity to consider relevant
    
    Returns:
        Dictionary with evolution points, drift points, and max drift
    """
    # Embed the concept
    concept_embedding = embed_text(concept)
    embedding_str = '[' + ','.join(map(str, concept_embedding)) + ']'
    
    # Fetch relevant embeddings grouped by period
    pool = await get_pool()
    
    # Map granularity to PostgreSQL date_trunc format
    trunc_map = {
        'month': 'month',
        'week': 'week',
        'day': 'day'
    }
    trunc_period = trunc_map.get(granularity, 'month')
    
    sql = f"""
    SELECT
      date_trunc('{trunc_period}', rtm.published_at) AS period,
      st.embedding,
      1 - (st.embedding <=> $1::vector) AS similarity
    FROM speech_turns st
    INNER JOIN raw_transcripts_meta rtm ON st.doc_id = rtm.doc_id
    WHERE
      rtm.published_at IS NOT NULL
      AND rtm.published_at >= $2
      AND rtm.published_at <= $3
      AND (st.embedding <=> $1::vector) < $4  -- Use distance operator for better index usage
    ORDER BY similarity DESC
    LIMIT 10000;  -- Limit results to prevent extremely long queries
    """
    
    async with pool.acquire() as conn:
        # Convert similarity threshold to distance (1 - similarity)
        distance_threshold = 1 - similarity_threshold
        rows = await conn.fetch(
            sql,
            embedding_str,
            start_date,
            end_date,
            distance_threshold
        )
    
    if not rows:
        return {
            "concept": concept,
            "granularity": granularity,
            "points": [],
            "drift": [],
            "max_drift": None
        }
    
    # Group embeddings by period using analytics module
    embeddings_by_period, counts_by_period = group_embeddings_by_period(rows, granularity)
    
    centroids = compute_centroids(embeddings_by_period)
    concept_vec = np.array(concept_embedding)
    
    # Compute evolution points and drift using analytics module
    evolution_points = compute_evolution_points(centroids, concept_vec, counts_by_period)
    drift_points = compute_drift(centroids)
    
    # Find max drift
    max_drift = None
    if drift_points:
        max_drift_point = max(drift_points, key=lambda x: x["semantic_change"])
        max_drift = max_drift_point
    
    return {
        "concept": concept,
        "granularity": granularity,
        "points": evolution_points,
        "drift": drift_points,
        "max_drift": max_drift
    }
