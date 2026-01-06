import numpy as np
import json
from datetime import datetime, timedelta
from backend.utils.postprocessing_helpers import embed_text
from backend.analytics.drift import (
    fetch_sentences,
    top_sentences,
    calculate_semantic_change,
    explain_semantic_drift_with_llm
)



async def explain_drift_service(
    concept: str,
    from_period: str,
    to_period: str,
    max_examples: int = 10,
    similarity_threshold: float = 0.6
):
    """
    Main service function to explain semantic drift between two periods.
    
    Args:
        concept: The concept to analyze
        from_period: Period in YYYY-MM format
        to_period: Period in YYYY-MM format
        max_examples: Maximum number of examples per period
    
    Returns:
        Dictionary with drift explanation in new format
    """
    # Get concept embedding
    concept_embedding = embed_text(concept)
    
    # Parse periods and create date ranges (full month)
    from_date = datetime.strptime(f"{from_period}-01", "%Y-%m-%d")
    to_date = datetime.strptime(f"{to_period}-01", "%Y-%m-%d")
    
    # Calculate proper end of month dates
    # For from_period: get start of next month - 1 day
    from_year, from_month = from_date.year, from_date.month
    if from_month == 12:
        from_end = datetime(from_year + 1, 1, 1) - timedelta(days=1)
    else:
        from_end = datetime(from_year, from_month + 1, 1) - timedelta(days=1)
    
    # For to_period: get start of next month - 1 day
    to_year, to_month = to_date.year, to_date.month
    if to_month == 12:
        to_end = datetime(to_year + 1, 1, 1) - timedelta(days=1)
    else:
        to_end = datetime(to_year, to_month + 1, 1) - timedelta(days=1)
    
    pre_range = (from_date.strftime("%Y-%m-%d"), from_end.strftime("%Y-%m-%d"))
    post_range = (to_date.strftime("%Y-%m-%d"), to_end.strftime("%Y-%m-%d"))
    
    # Fetch more sentences for accurate drift calculation, but limit examples for LLM
    # Use at least 50 results for drift calculation to match semantic_evolution behavior
    fetch_limit = max(100, max_examples * 10)
    
    # Fetch sentences for both periods
    pre_rows = await fetch_sentences(concept_embedding, pre_range, similarity_threshold=similarity_threshold, top_k=fetch_limit)
    post_rows = await fetch_sentences(concept_embedding, post_range, similarity_threshold=similarity_threshold, top_k=fetch_limit)
    
    # Get top sentences
    pre_top_sentences = top_sentences(pre_rows, n=max_examples)
    post_top_sentences = top_sentences(post_rows, n=max_examples)
    
    # Calculate semantic change
    if not pre_rows or not post_rows:
        semantic_change = 0.0
    else:
        pre_embeddings = [
            np.array(json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"]) 
            for r in pre_rows
        ]
        post_embeddings = [
            np.array(json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"]) 
            for r in post_rows
        ]
        semantic_change = calculate_semantic_change(pre_embeddings, post_embeddings)
    
    # Get LLM structured analysis
    analysis = explain_semantic_drift_with_llm(
        concept=concept,
        drift_score=semantic_change,
        pre_sentences=pre_top_sentences,
        post_sentences=post_top_sentences
    )
    
    # Format response - keep complete LLM response
    return {
        "concept": concept,
        "from_period": from_period,
        "to_period": to_period,
        "semantic_change": round(semantic_change, 2),
        "response": analysis
    }

