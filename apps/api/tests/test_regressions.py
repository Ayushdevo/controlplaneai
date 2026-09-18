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


@pytest.mark.parametrize("text, expected", [
    ('Mail a@b.co then call +1 212 555 0199 please', 'Mail [EMAIL_REDACTED] then call [PHONE_REDACTED] please'),
    ('Card 4111 1111 1111 1111 end', 'Card [CREDIT_CARD_REDACTED] end'),
])
def test_redaction_uses_original_nonoverlapping_spans(text, expected):
    result, redacted = detect_pii(text)
    assert redacted == expected
    assert len(result.metadata['entities']) == expected.count('_REDACTED]')
