import re

from app.schemas.evaluation import DetectorResult, Evidence, Severity


SIGNATURES = {
    "instruction_override": re.compile(r"\b(ignore|disregard|bypass)\b.{0,30}\b(previous|system|developer|safety)\b", re.I | re.S),
    "prompt_extraction": re.compile(r"\b(reveal|show|print|extract)\b.{0,30}\b(system prompt|hidden instructions)\b", re.I | re.S),
    "role_hijack": re.compile(r"\b(?:you are now|act as an unrestricted|jailbreak)\b", re.I | re.S),
}


def detect_injection(text: str) -> DetectorResult:
    # PDF and chat wrapping must not split fixed attack phrases.
    normalized = " ".join(text.split())
    matches = [name for name, pattern in SIGNATURES.items() if pattern.search(normalized)]
    detected = bool(matches)
    score = min(1.0, 0.62 + (0.12 * len(matches))) if detected else 0.02
    return DetectorResult(
        category="injection",
        score=score,
        confidence=0.91 if detected else 0.88,
        severity=Severity.HIGH if detected else Severity.LOW,
        detected=detected,
        evidence=[Evidence(label="Attack signature", detail=name.replace("_", " ").title()) for name in matches],
        metadata={"attack_type": matches[0] if matches else None},
    )

