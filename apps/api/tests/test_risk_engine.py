from app.risk.engine import calculate_risk
from app.schemas.evaluation import Decision, DetectorResult, Severity


BASE_POLICY = {
    "weights": {"privacy": 1.0, "injection": 1.0, "hallucination": 1.0},
    "rules": {"require_grounding": False},
    "thresholds": {"modify": 30, "review": 60, "block": 85},
}


def detector(category: str, score: float, *, detected: bool = True) -> DetectorResult:
    return DetectorResult(
        category=category,
        score=score,
        confidence=0.9,
        severity=Severity.HIGH,
        detected=detected,
    )


def test_risk_uses_weighted_detector_scores():
    risk, _, decision, _ = calculate_risk(
        [detector("privacy", 0.9), detector("injection", 0.3), detector("hallucination", 0.0)],
        BASE_POLICY,
    )

    assert risk == 40
    assert decision == Decision.MODIFY


def test_prompt_injection_detection_applies_minimum_risk_floor():
    risk, _, decision, reasons = calculate_risk(
        [detector("privacy", 0.0, detected=False), detector("injection", 0.1)],
        BASE_POLICY,
    )

    assert risk >= 65
    assert decision == Decision.HUMAN_REVIEW
    assert any("containment" in reason.lower() for reason in reasons)


def test_privacy_detection_applies_minimum_risk_floor():
    risk, _, decision, reasons = calculate_risk(
        [detector("privacy", 0.1)],
        BASE_POLICY,
    )

    assert risk >= 45
    assert decision == Decision.MODIFY
    assert any("sensitive data" in reason.lower() for reason in reasons)


def test_grounding_policy_can_force_review_floor():
    policy = {
        **BASE_POLICY,
        "rules": {"require_grounding": True},
    }

    risk, _, decision, reasons = calculate_risk(
        [detector("hallucination", 0.1)],
        policy,
    )

    assert risk >= 60
    assert decision == Decision.HUMAN_REVIEW
    assert any("evidence" in reason.lower() for reason in reasons)


def test_no_detectors_returns_safe_default():
    risk, confidence, decision, reasons = calculate_risk([], BASE_POLICY)

    assert risk == 0
    assert confidence == 0.88
    assert decision == Decision.ALLOW
    assert reasons == []
