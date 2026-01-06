from fastapi import APIRouter, HTTPException
from backend.app.models.search import SearchRequest, SearchResponse
from backend.app.services.search_service import semantic_search

router = APIRouter(tags=["semantic-search"])

@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    result = await semantic_search(req.question, req.top_k)

    if result is None or len(result) == 0:
        raise HTTPException(status_code=404, detail="No documents found")

    return {
        "question": req.question,
        "results": result
    }
