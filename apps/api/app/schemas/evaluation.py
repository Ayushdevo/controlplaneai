from datetime import datetime
from enum import Enum
from typing import Any, Literal, Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Decision(str, Enum):
    ALLOW = "ALLOW"
    MODIFY = "MODIFY"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    BLOCK = "BLOCK"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvaluationRequest(BaseModel):
    application: Literal["support", "knowledge", "financial"] = "support"
    input: str = Field(min_length=1, max_length=12000)
    output: str = Field(default="", max_length=20000)
    context: list[Annotated[str, Field(max_length=20000)]] = Field(default_factory=list, max_length=50)
    conversation_id: str | None = None
    request_id: str | None = Field(default=None, max_length=128)


    @field_validator("input")
    @classmethod
    def reject_blank_input(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("input must contain non-whitespace text")
        return value


class Evidence(BaseModel):
    label: str
    detail: str
    support: str | None = None
    similarity: float | None = None


class DetectorResult(BaseModel):
    category: str
    score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    severity: Severity
    detected: bool
    evidence: list[Evidence] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationResponse(BaseModel):
    audit_id: UUID = Field(default_factory=uuid4)
    decision: Decision
    risk_score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    reasons: list[str]
    triggered_policies: list[str]
    detectors: list[DetectorResult]
    evidence_coverage: int = Field(ge=0, le=100)
    latency_ms: int
    detectors_run: list[str]
    model_calls: int = 0
    estimated_cost: float = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    redacted_output: str | None = None
    request_id: str | None = None
    conversation_id: str | None = None
    application: str
    recommended_action: str
    policy_name: str
    conversation_risk: float = Field(default=0, ge=0, le=1)
    human_override: dict[str, Any] | None = None
