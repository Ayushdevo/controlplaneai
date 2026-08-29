POLICIES = {
    "support": {"name": "Customer Support AI", "risk_tolerance": "moderate", "latency_budget_ms": 300, "weights": {"privacy": 1.0, "injection": 0.9, "hallucination": 0.55, "bias": 0.55}, "thresholds": {"modify": 41, "review": 61, "block": 81}, "rules": {"redact_pii": True, "require_grounding": False, "human_review_high_risk": True}},
    "knowledge": {"name": "Internal Knowledge Copilot", "risk_tolerance": "guarded", "latency_budget_ms": 500, "weights": {"privacy": 1.0, "injection": 0.9, "hallucination": 0.95, "bias": 0.5}, "thresholds": {"modify": 36, "review": 56, "block": 76}, "rules": {"redact_pii": True, "require_grounding": True, "human_review_high_risk": True}},
    "financial": {"name": "Financial Decision Assistant", "risk_tolerance": "low", "latency_budget_ms": 800, "weights": {"privacy": 1.0, "injection": 0.95, "hallucination": 1.0, "bias": 0.85}, "thresholds": {"modify": 31, "review": 51, "block": 71}, "rules": {"redact_pii": True, "require_grounding": True, "human_review_high_risk": True}},
}


def get_policy(application: str) -> dict:
    return POLICIES.get(application, POLICIES["support"])
