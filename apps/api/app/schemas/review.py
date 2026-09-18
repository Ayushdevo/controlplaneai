from datetime import datetime
from enum import Enum
from uuid import UUID

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    BLOCK = "BLOCK"
    MODIFY = "MODIFY"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    NEEDS_INVESTIGATION = "NEEDS_INVESTIGATION"


class ReviewRequest(BaseModel):
    audit_id: UUID
    reviewer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=200)]
    decision: ReviewDecision
    comment: str = Field(default="", max_length=2000)


class ReviewRecord(ReviewRequest):
    timestamp: datetime
    previous_decision: str
