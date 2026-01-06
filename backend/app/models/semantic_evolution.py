from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class SemanticEvolutionRequest(BaseModel):
    concept: str
    granularity: str = "month"
    start_date: date
    end_date: date
    similarity_threshold: float = 0.6


class EvolutionPoint(BaseModel):
    period: str
    centroid_similarity: float
    num_chunks: int


class DriftPoint(BaseModel):
    from_period: str = Field(alias='from')
    to: str
    semantic_change: float

    class Config:
        # Allow using 'from' as a field name
        populate_by_name = True


class MaxDrift(BaseModel):
    from_period: str = Field(alias='from')
    to: str
    semantic_change: float

    class Config:
        populate_by_name = True


class SemanticEvolutionResponse(BaseModel):
    concept: str
    granularity: str
    points: List[EvolutionPoint]
    drift: List[DriftPoint]
    max_drift: Optional[MaxDrift]
