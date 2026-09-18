from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints
from .evaluation import Decision


class ActionRequest(BaseModel):
    agent_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=200)]
    action: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True, min_length=2, max_length=100)]
    parameters: dict = Field(default_factory=dict)


class ActionResponse(BaseModel):
    decision: Decision
    risk_score: int
    reason: str
