from pydantic import BaseModel, Field
from .evaluation import Decision


class ActionRequest(BaseModel):
    agent_id: str = Field(min_length=2)
    action: str = Field(min_length=2)
    parameters: dict = Field(default_factory=dict)


class ActionResponse(BaseModel):
    decision: Decision
    risk_score: int
    reason: str
