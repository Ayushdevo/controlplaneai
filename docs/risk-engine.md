# Risk engine

Detector scores are normalized from 0 to 1. Application policies provide category weights and thresholds. The weighted sum is normalized to 0-100 and mapped to a decision, so the same interaction can produce different outcomes under different applications.

The engine also applies explainable safety floors: detected PII requires at least a remediation score, prompt injection requires containment, and policies with `require_grounding` route unsupported responses to human review. When a `conversation_id` is supplied, the prior highest risk score in that conversation increases the current score. Scores are qualitative control signals, not calibrated probabilities.

Demo detectors are deterministic regex/token-overlap heuristics. They are intentionally not represented as LLM judgments or production-grade safety detection.
