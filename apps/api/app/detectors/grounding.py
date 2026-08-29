from app.schemas.evaluation import DetectorResult, Evidence, Severity


def evaluate_grounding(output: str, context: list[str]) -> DetectorResult:
    if not output:
        return DetectorResult(category="hallucination", score=0, confidence=0.65, severity=Severity.LOW, detected=False)
    output_terms = {term.lower() for term in output.split() if len(term) > 4}
    context_terms = {term.lower() for source in context for term in source.split() if len(term) > 4}
    overlap = len(output_terms & context_terms) / max(1, len(output_terms))
    grounding = min(1.0, overlap + (0.25 if context else 0))
    unsupported = grounding < 0.55
    return DetectorResult(
        category="hallucination",
        score=round(1 - grounding, 3),
        confidence=0.82,
        severity=Severity.MEDIUM if unsupported else Severity.LOW,
        detected=unsupported,
        evidence=[Evidence(label="Evidence coverage", detail="Potentially unsupported claim; compare with retrieved sources", support="partial" if context else "unsupported", similarity=round(grounding, 2))],
        metadata={"grounding_score": round(grounding, 3), "unsupported_claims": 1 if unsupported else 0},
    )
