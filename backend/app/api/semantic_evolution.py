from fastapi import APIRouter, HTTPException
from backend.app.models.semantic_evolution import (
    SemanticEvolutionRequest,
    SemanticEvolutionResponse
)
from backend.app.services.semantic_evolution_service import compute_semantic_evolution

router = APIRouter(tags=["semantic-evolution"])


@router.post("/semantic-evolution", response_model=SemanticEvolutionResponse)
async def semantic_evolution(req: SemanticEvolutionRequest):
    """
    Compute semantic evolution metrics for a concept over time.
    
    Returns:
        - Evolution points showing centroid similarity and chunk count per period
        - Drift measurements between consecutive periods
        - Maximum drift point
    """
    try:
        result = await compute_semantic_evolution(
            concept=req.concept,
            granularity=req.granularity,
            start_date=req.start_date,
            end_date=req.end_date,
            similarity_threshold=req.similarity_threshold
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing semantic evolution: {str(e)}")
