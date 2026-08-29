from app.schemas.evaluation import DetectorResult, Evidence, Severity


def detect_bias(text: str) -> DetectorResult:
    markers = [term for term in ("always", "never", "women", "men", "old people", "foreigners") if term in text.lower()]
    detected = bool(markers)
    return DetectorResult(
        category="bias",
        score=0.58 if detected else 0.04,
        confidence=0.71 if detected else 0.83,
        severity=Severity.MEDIUM if detected else Severity.LOW,
        detected=detected,
        evidence=[Evidence(label="Evaluation dimension", detail="Potential gender or generalization bias; requires contextual review") for _ in markers[:1]],
        metadata={"dimension": "gender/generalization" if detected else None},
    )
