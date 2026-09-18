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
    candidates = [
        (match.start(), match.end(), entity_type, confidence)
        for entity_type, (pattern, confidence) in PATTERNS.items()
        for match in pattern.finditer(text)
    ]
    spans = []
    for start, end, entity_type, confidence in sorted(candidates, key=lambda item: (-item[3], item[0])):
        if not any(start < other_end and end > other_start for other_start, other_end, *_ in spans):
            spans.append((start, end, entity_type, confidence))
    redacted = text
    for start, end, entity_type, confidence in sorted(spans, reverse=True):
        entities.append({"type": entity_type, "confidence": confidence})
        redacted = redacted[:start] + f"[{entity_type}_REDACTED]" + redacted[end:]
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
