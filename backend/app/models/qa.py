from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5

class Source(BaseModel):
    doc_id: str
    sequence: int | None
    similarity: float

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

