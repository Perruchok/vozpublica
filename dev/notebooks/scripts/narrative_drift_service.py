async def analyze_concept_drift_service(
    concept: str,
    pre_range: tuple[str, str],
    post_range: tuple[str, str],
    similarity_threshold: float = 0.6,
):
    concept_embedding = embed_text(concept)

    relevant_embeddings = await fetch_relevant_embeddings(
        concept_embedding,
        similarity_threshold
    )

    embeddings_by_period = group_by_period(relevant_embeddings)
    period_embeddings = {
        period: average_embedding(vectors)
        for period, vectors in embeddings_by_period.items()
    }

    drift_over_time = semantic_drift(period_embeddings)

    pre_rows = await fetch_sentences(concept_embedding, pre_range, similarity_threshold)
    post_rows = await fetch_sentences(concept_embedding, post_range, similarity_threshold)

    pre_top = top_sentences(pre_rows, n=10)
    post_top = top_sentences(post_rows, n=10)

    pre_grouped = group_embeddings_by_speaker(pre_rows)
    post_grouped = group_embeddings_by_speaker(post_rows)

    pre_avg = average_embeddings(pre_grouped, min_evidence=2)
    post_avg = average_embeddings(post_grouped, min_evidence=2)

    speaker_drifts = speaker_drift(pre_avg, post_avg)

    overall_drift = cosine_distance(
        average_embedding(list(pre_avg.values())),
        average_embedding(list(post_avg.values()))
    )

    explanation = explain_semantic_drift(
        concept=concept,
        drift_score=overall_drift,
        pre_sentences=pre_top,
        post_sentences=post_top
    )

    return {
        "concept": concept,
        "overall_drift": float(overall_drift),
        "drift_over_time": drift_over_time,
        "speaker_drifts": speaker_drifts,
        "pre_top_sentences": pre_top,
        "post_top_sentences": post_top,
        "explanation": explanation,
    }
