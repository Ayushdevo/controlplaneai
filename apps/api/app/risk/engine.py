from app.schemas.evaluation import Decision, DetectorResult


def calculate_risk(detectors: list[DetectorResult], policy: dict) -> tuple[int, float, Decision, list[str]]:
    scores = {detector.category: detector.score for detector in detectors}
    weights = policy["weights"]
    total_weight = sum(weights.values())
    weighted = sum(scores.get(category, 0) * weight for category, weight in weights.items())
    risk = round((weighted / total_weight) * 100) if total_weight else 0
    privacy = next((item for item in detectors if item.category == "privacy"), None)
    injection = next((item for item in detectors if item.category == "injection"), None)
    grounding = next((item for item in detectors if item.category == "hallucination"), None)
    floors: list[tuple[int, str]] = []
    if privacy and privacy.detected:
        floors.append((45, "Sensitive data requires remediation"))
    if injection and injection.detected:
        floors.append((65, "Prompt-injection attempt requires containment"))
    if policy["rules"].get("require_grounding") and grounding and grounding.detected:
        floors.append((policy["thresholds"]["review"], "Policy requires evidence for this use case"))
    if floors:
        risk = max(risk, max(floor for floor, _ in floors))
    thresholds = policy["thresholds"]
    if risk >= thresholds["block"]:
        decision = Decision.BLOCK
    elif risk >= thresholds["review"]:
        decision = Decision.HUMAN_REVIEW
    elif risk >= thresholds["modify"]:
        decision = Decision.MODIFY
    else:
        decision = Decision.ALLOW
    active = [detector for detector in detectors if detector.detected]
    confidence = round(sum(detector.confidence for detector in active) / len(active), 2) if active else 0.88
    reasons = [f"{detector.category.title()} signal detected ({detector.confidence:.0%} confidence)" for detector in active]
    reasons.extend(reason for _, reason in floors)
    return risk, confidence, decision, reasons
