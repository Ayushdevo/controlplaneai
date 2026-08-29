from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    BLOCK = "BLOCK"
    MODIFY = "MODIFY"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    NEEDS_INVESTIGATION = "NEEDS_INVESTIGATION"


class ReviewRequest(BaseModel):
    audit_id: UUID
    reviewer: str = Field(min_length=2)
    decision: ReviewDecision
    comment: str = Field(default="", max_length=2000)


class ReviewRecord(ReviewRequest):
    timestamp: datetime
    previous_decision: str
