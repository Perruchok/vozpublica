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
    import time
    from asyncpg.exceptions import QueryCanceledError, TooManyConnectionsError
    
    try:
        print(f"[semantic_evolution] Request: concept='{req.concept}', granularity={req.granularity}, "
              f"start_date={req.start_date}, end_date={req.end_date}, threshold={req.similarity_threshold}")
        
        start_time = time.time()
        
        result = await compute_semantic_evolution(
            concept=req.concept,
            granularity=req.granularity,
            start_date=req.start_date,
            end_date=req.end_date,
            similarity_threshold=req.similarity_threshold
        )
        
        elapsed = time.time() - start_time
        print(f"[semantic_evolution] Completed in {elapsed:.2f}s: {len(result.get('drift', []))} drift points, "
              f"{len(result.get('points', []))} evolution points")
        
        return result
    
    except TimeoutError:
        print(f"[semantic_evolution] Query timeout - consider using a higher similarity_threshold or shorter date range")
        raise HTTPException(
            status_code=504,
            detail="Query timeout: The analysis took too long. Try using a higher similarity_threshold (e.g., 0.75) or a shorter date range."
        )
    
    except QueryCanceledError:
        print(f"[semantic_evolution] Query canceled by database")
        raise HTTPException(
            status_code=504,
            detail="Query canceled: The analysis exceeded database limits. Try narrowing your search parameters."
        )
    
    except TooManyConnectionsError:
        print(f"[semantic_evolution] Too many database connections")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable. Please try again in a moment."
        )
        
    except Exception as e:
        print(f"[semantic_evolution] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error computing semantic evolution: {str(e)}")
