# Architecture

Requests enter FastAPI through versioned endpoints and are processed by independent detector services. Deterministic PII and injection checks run first. Output grounding uses a local evidence catalogue in demo mode. The risk engine combines category scores with application policy weights, then the decision engine maps normalized risk to ALLOW, MODIFY, HUMAN_REVIEW, or BLOCK.

Every evaluation returns structured evidence, detector confidence, policy triggers, latency metadata, and an audit identifier. The frontend consumes these contracts and keeps business logic in API services rather than React components.
