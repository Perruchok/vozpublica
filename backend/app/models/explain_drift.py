from pydantic import BaseModel, Field
from typing import List


class ExplainDriftRequest(BaseModel):
    concept: str
    from_period: str = Field(..., description="Period in YYYY-MM format", pattern=r"^\d{4}-\d{2}$")
    to_period: str = Field(..., description="Period in YYYY-MM format", pattern=r"^\d{4}-\d{2}$")
    max_examples: int = Field(default=10, ge=1, le=50, description="Maximum examples to retrieve")
    similarity_threshold: float = Field(default=0.6, ge=0.0, le=1.0, description="Minimum similarity to concept")


class CoreFraming(BaseModel):
    first_period: str = Field(..., description="Description of concept framing in first period with citations")
    second_period: str = Field(..., description="Description of concept framing in second period with citations")


class DriftAnalysis(BaseModel):
    core_framing: CoreFraming = Field(..., description="How the concept is framed in each period")
    gained_prominence: List[str] = Field(..., description="Concepts that gained prominence")
    lost_prominence: List[str] = Field(..., description="Concepts that lost prominence")
    overall_shift: str = Field(..., description="Overall semantic shift explanation with citations")


class ExplainDriftResponse(BaseModel):
    concept: str
    from_period: str
    to_period: str
    semantic_change: float
    response: DriftAnalysis = Field(..., description="LLM analysis response with citations")
