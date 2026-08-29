import re

from app.schemas.evaluation import DetectorResult, Evidence, Severity


SIGNATURES = {
    "instruction_override": re.compile(r"(ignore|disregard|bypass).{0,30}(previous|system|developer|safety)", re.I),
    "prompt_extraction": re.compile(r"(reveal|show|print|extract).{0,30}(system prompt|hidden instructions)", re.I),
    "role_hijack": re.compile(r"you are now|act as an unrestricted|jailbreak", re.I),
}


def detect_injection(text: str) -> DetectorResult:
    matches = [name for name, pattern in SIGNATURES.items() if pattern.search(text)]
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
