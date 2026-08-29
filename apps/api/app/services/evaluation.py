from time import perf_counter
from uuid import uuid4

from app.detectors.bias import detect_bias
from app.detectors.grounding import evaluate_grounding
from app.detectors.injection import detect_injection
from app.detectors.pii import detect_pii
from app.policies.catalog import get_policy
from app.risk.engine import calculate_risk
from app.schemas.evaluation import Decision, EvaluationRequest, EvaluationResponse
from app.services.demo_store import store


class EvaluationService:
    def evaluate(self, request: EvaluationRequest) -> EvaluationResponse:
        started = perf_counter()
        policy = get_policy(request.application)
        input_pii, redacted_input = detect_pii(request.input)
        output_pii, redacted_output = detect_pii(request.output)
        injection = detect_injection("\n".join([request.input, *request.context]))
        grounding = evaluate_grounding(request.output, request.context)
        bias = detect_bias(request.output)
        detectors = [input_pii, output_pii, injection, grounding, bias]
        prior_risk = store.conversation_risk(request.conversation_id)
        risk, confidence, decision, reasons = calculate_risk(detectors, policy)
        if prior_risk >= 0.45:
            risk = min(100, risk + round(prior_risk * 20))
            reasons.append("Prior conversation risk increased this turn's score")
            if risk >= policy["thresholds"]["review"] and decision in (Decision.ALLOW, Decision.MODIFY):
                decision = Decision.HUMAN_REVIEW
        if input_pii.detected or output_pii.detected:
            reasons.insert(0, "Sensitive values were detected and withheld from audit details")
        coverage = round((1 - grounding.score) * 100)
        return EvaluationResponse(
            audit_id=uuid4(), decision=decision, risk_score=risk, confidence=confidence,
            reasons=reasons or ["No elevated risk signals detected"],
            triggered_policies=[f"CP-{request.application.upper()}-BASELINE"], detectors=detectors,
            evidence_coverage=coverage, latency_ms=max(1, round((perf_counter() - started) * 1000)),
            detectors_run=[detector.category for detector in detectors], redacted_output=redacted_output if output_pii.detected else None,
            request_id=request.request_id, conversation_id=request.conversation_id, application=request.application, policy_name=policy["name"],
            recommended_action={Decision.ALLOW: "Allow response", Decision.MODIFY: "Redact sensitive values before release", Decision.HUMAN_REVIEW: "Route to a qualified reviewer before release", Decision.BLOCK: "Block delivery and investigate the signal"}[decision],
            conversation_risk=round(prior_risk, 2),
        )
