import pytest

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


def test_risk_uses_equal_weight_detector_scores():
    risk, _, decision, _ = calculate_risk(
        [
            detector("privacy", 0.9, detected=False),
            detector("injection", 0.3, detected=False),
            detector("hallucination", 0.0, detected=False),
        ],
        BASE_POLICY,
    )

    assert risk == 40
    assert decision == Decision.MODIFY


def test_prompt_injection_detection_applies_minimum_risk_floor():
    risk, _, decision, reasons = calculate_risk(
        [detector("privacy", 0.0, detected=False), detector("injection", 0.1)],
        BASE_POLICY,
    )

    assert risk == 65
    assert decision == Decision.HUMAN_REVIEW
    assert any("containment" in reason.lower() for reason in reasons)


def test_privacy_detection_applies_minimum_risk_floor():
    risk, _, decision, reasons = calculate_risk(
        [detector("privacy", 0.1)],
        BASE_POLICY,
    )

    assert risk == 45
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

    assert risk == 60
    assert decision == Decision.HUMAN_REVIEW
    assert any("evidence" in reason.lower() for reason in reasons)


def test_no_detectors_returns_safe_default():
    risk, confidence, decision, reasons = calculate_risk([], BASE_POLICY)

    assert risk == 0
    assert confidence == 0.88
    assert decision == Decision.ALLOW
    assert reasons == []


def test_risk_respects_unequal_policy_weights():
    policy = {**BASE_POLICY, "weights": {"privacy": 3.0, "injection": 1.0, "hallucination": 1.0}}
    risk, _, decision, _ = calculate_risk(
        [
            detector("privacy", 0.9, detected=False),
            detector("injection", 0.3, detected=False),
            detector("hallucination", 0.0, detected=False),
        ],
        policy,
    )
    # (0.9 * 3 + 0.3 * 1 + 0.0 * 1) / 5 * 100 = 60.
    assert risk == 60
    assert decision == Decision.HUMAN_REVIEW


def test_detection_floors_do_not_reduce_high_weighted_risk():
    risk, _, decision, _ = calculate_risk(
        [detector(category, 0.9) for category in BASE_POLICY["weights"]],
        BASE_POLICY,
    )
    assert risk == 90
    assert decision == Decision.BLOCK


def test_confidence_averages_only_active_detectors():
    active_privacy = detector("privacy", 0.1)
    active_privacy.confidence = 0.8
    inactive_grounding = detector("hallucination", 0.1, detected=False)
    inactive_grounding.confidence = 0.1
    active_injection = detector("injection", 0.1)
    active_injection.confidence = 0.6

    _, confidence, _, _ = calculate_risk(
        [active_privacy, inactive_grounding, active_injection],
        BASE_POLICY,
    )

    assert confidence == 0.7


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (29, Decision.ALLOW),
        (30, Decision.MODIFY),
        (31, Decision.MODIFY),
        (59, Decision.MODIFY),
        (60, Decision.HUMAN_REVIEW),
        (61, Decision.HUMAN_REVIEW),
        (84, Decision.HUMAN_REVIEW),
        (85, Decision.BLOCK),
        (86, Decision.BLOCK),
    ],
)
def test_threshold_boundaries(score, expected):
    # Isolate decision thresholds from rounding and detection floors.
    policy = {**BASE_POLICY, "weights": {"hallucination": 1.0}}

    risk, _, decision, _ = calculate_risk(
        [detector("hallucination", score / 100, detected=False)],
        policy,
    )

    assert risk == score
    assert decision == expected
