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
        print(f"[semantic_evolution] Request: concept='{req.concept}', granularity={req.granularity}, "
              f"start_date={req.start_date}, end_date={req.end_date}, threshold={req.similarity_threshold}")
        
        result = await compute_semantic_evolution(
            concept=req.concept,
            granularity=req.granularity,
            start_date=req.start_date,
            end_date=req.end_date,
            similarity_threshold=req.similarity_threshold
        )
        
        print(f"[semantic_evolution] Result: {len(result.get('drift', []))} drift points, "
              f"{len(result.get('points', []))} evolution points")
        
        return result
        
    except Exception as e:
        print(f"[semantic_evolution] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error computing semantic evolution: {str(e)}")
