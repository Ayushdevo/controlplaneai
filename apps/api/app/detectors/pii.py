import re

from app.schemas.evaluation import DetectorResult, Evidence, Severity


PATTERNS = {
    "EMAIL": (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), 0.96),
    "PHONE": (re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{8,}\d)(?!\d)"), 0.92),
    "CREDIT_CARD": (re.compile(r"(?<!\d)(?:\d[ -]*?){13,16}(?!\d)"), 0.98),
    "GOVERNMENT_ID": (re.compile(r"\b[A-Z]{1,3}-?\d{6,12}\b"), 0.82),
}


def detect_pii(text: str) -> tuple[DetectorResult, str]:
    entities: list[dict] = []
    redacted = text
    for entity_type, (pattern, confidence) in PATTERNS.items():
        matches = list(pattern.finditer(text))
        for match in reversed(matches):
            entities.append({"type": entity_type, "confidence": confidence})
            redacted = redacted[: match.start()] + f"[{entity_type}_REDACTED]" + redacted[match.end() :]
    detected = bool(entities)
    result = DetectorResult(
        category="privacy",
        score=min(1.0, 0.45 + 0.18 * len(entities)) if detected else 0.0,
        confidence=max((item["confidence"] for item in entities), default=0.97),
        severity=Severity.CRITICAL if detected else Severity.LOW,
        detected=detected,
        evidence=[Evidence(label="Sensitive entity", detail=f"{item['type']} detected; value withheld from logs") for item in entities],
        metadata={"entities": entities},
    )
    return result, redacted
