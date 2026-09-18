import pytest

from app.detectors.pii import detect_pii
from app.policies.catalog import get_policy
from app.risk.engine import calculate_risk


def test_input_privacy_is_not_overwritten_by_clean_output():
    private, _ = detect_pii('Contact jane@example.com')
    clean, _ = detect_pii('Hello')
    assert calculate_risk([private, clean], get_policy('support'))[:3] == calculate_risk(
        [clean, private], get_policy('support')
    )[:3]
