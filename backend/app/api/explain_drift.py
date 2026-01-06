from fastapi import APIRouter, HTTPException
from backend.app.models.explain_drift import (
    ExplainDriftRequest,
    ExplainDriftResponse
)
from backend.app.services.explain_drift_service import explain_drift_service

router = APIRouter(tags=["explain-drift"])


@router.post("/explain-drift", response_model=ExplainDriftResponse)
async def explain_drift(req: ExplainDriftRequest):
    """
    Explain semantic drift for a concept between two time periods.
    
    Analyzes how the discourse around a concept has shifted by:
    1. Comparing semantic embeddings between periods
    2. Identifying key drivers of change
    3. Providing contrasting examples from each period
    
    Args:
        req: Request containing:
            - concept: The concept to analyze
            - from_period: First period (YYYY-MM)
            - to_period: Second period (YYYY-MM)
            - max_examples: Number of examples per period (default: 10)
    
    Returns:
        ExplainDriftResponse with:
            - semantic_change: Cosine distance between periods
            - response: Complete LLM analysis with citations and references
    """
    try:
        result = await explain_drift_service(
            concept=req.concept,
            from_period=req.from_period,
            to_period=req.to_period,
            max_examples=req.max_examples,
            similarity_threshold=req.similarity_threshold
        )
        
        return ExplainDriftResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error explaining semantic drift: {str(e)}"
        )
