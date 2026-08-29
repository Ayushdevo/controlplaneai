from collections import Counter
from uuid import UUID

from app.schemas.evaluation import EvaluationResponse
from app.schemas.review import ReviewRecord, ReviewRequest


class DemoStore:
    def __init__(self) -> None:
        self.evaluations: dict[UUID, EvaluationResponse] = {}
        self.reviews: list[ReviewRecord] = []

    def save_evaluation(self, evaluation: EvaluationResponse) -> EvaluationResponse:
        self.evaluations[evaluation.audit_id] = evaluation
        return evaluation

    def list_incidents(self) -> list[EvaluationResponse]:
        return [item for item in self.evaluations.values() if item.decision != "ALLOW"]

    def get_evaluation(self, audit_id: UUID) -> EvaluationResponse | None:
        return self.evaluations.get(audit_id)

    def add_review(self, request: ReviewRequest, previous_decision: str) -> ReviewRecord:
        record = ReviewRecord(**request.model_dump(), timestamp=__import__("datetime").datetime.now(__import__("datetime").timezone.utc), previous_decision=previous_decision)
        self.reviews.append(record)
        evaluation = self.evaluations.get(request.audit_id)
        if evaluation:
            final = {"APPROVE": "ALLOW", "BLOCK": "BLOCK", "MODIFY": "MODIFY", "FALSE_POSITIVE": "ALLOW", "NEEDS_INVESTIGATION": "HUMAN_REVIEW"}[request.decision.value]
            evaluation.decision = final
            evaluation.human_override = {"reviewer": request.reviewer, "decision": request.decision.value, "comment": request.comment, "timestamp": record.timestamp.isoformat(), "previous_decision": previous_decision}
        return record

    def conversation_risk(self, conversation_id: str | None) -> float:
        if not conversation_id:
            return 0.0
        values = [item.risk_score / 100 for item in self.evaluations.values() if item.conversation_id == conversation_id]
        return max(values, default=0.0)

    def analytics(self) -> dict:
        evaluations = list(self.evaluations.values())
        category_counts = Counter(
            detector.category
            for evaluation in evaluations
            for detector in evaluation.detectors
            if detector.detected
        )
        return {
            "evaluations": len(evaluations),
            "flagged": sum(item.decision != "ALLOW" for item in evaluations),
            "blocked": sum(item.decision == "BLOCK" for item in evaluations),
            "reviews": sum(item.decision == "HUMAN_REVIEW" for item in evaluations),
            "human_overrides": len(self.reviews),
            "allowed": sum(item.decision == "ALLOW" for item in evaluations),
            "average_risk_score": round(sum(item.risk_score for item in evaluations) / len(evaluations)) if evaluations else 0,
            "average_latency_ms": round(sum(item.latency_ms for item in evaluations) / len(evaluations)) if evaluations else 0,
            "categories": [{"name": name.title(), "value": value} for name, value in category_counts.items()],
            "trend": [],
        }


store = DemoStore()
