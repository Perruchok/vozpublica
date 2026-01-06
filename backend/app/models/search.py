from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    question: str
    top_k: int = 5

class SearchResult(BaseModel):
    doc_id: str
    speech_id: str
    text: str
    speaker_normalized: Optional[str]
    role: Optional[str]
    href: Optional[str]
    title: Optional[str]
    similarity: float

class SearchResponse(BaseModel):
    question: str
    results: List[SearchResult]
