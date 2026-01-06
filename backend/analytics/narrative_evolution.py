import numpy as np
from collections import defaultdict

def group_embeddings_by_period(rows, granularity):
    """
    Group embeddings by time period, parsing string format if needed.
    
    Returns:
        Tuple of (embeddings_by_period, counts_by_period)
    """
    embeddings_by_period = defaultdict(list)
    counts_by_period = defaultdict(int)

    for row in rows:
        period_key = row["period"].strftime(
            "%Y-%m" if granularity == "month" else "%Y-%m-%d"
        )
        
        # Parse embedding from string format if needed
        embedding_data = row["embedding"]
        if isinstance(embedding_data, str):
            # Remove brackets and parse as floats
            embedding_data = embedding_data.strip('[]').split(',')
            embedding = np.array([float(x) for x in embedding_data])
        else:
            embedding = np.array(embedding_data)
        
        embeddings_by_period[period_key].append(embedding)
        counts_by_period[period_key] += 1

    return dict(embeddings_by_period), dict(counts_by_period)


def compute_centroids(period_data):
    return {
        period: np.mean(vectors, axis=0)
        for period, vectors in period_data.items()
    }


def cosine_similarity(vec1, vec2):
    return float(
        np.dot(vec1, vec2) /
        (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    )


def compute_evolution_points(centroids, concept_vec, counts):
    points = []

    for period in sorted(centroids.keys()):
        sim = cosine_similarity(centroids[period], concept_vec)
        points.append({
            "period": period,
            "centroid_similarity": round(sim, 2),
            "num_chunks": counts[period]
        })

    return points


def compute_drift(centroids):
    periods = sorted(centroids.keys())
    drift = []

    for i in range(len(periods) - 1):
        sim = cosine_similarity(
            centroids[periods[i]],
            centroids[periods[i + 1]]
        )
        drift.append({
            "from": periods[i],
            "to": periods[i + 1],
            "semantic_change": round(1 - sim, 2)
        })

    return drift
