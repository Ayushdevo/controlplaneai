# ControlPlane.ai

ControlPlane.ai is a prototype AI runtime governance platform. It evaluates AI inputs, outputs, retrieved context, conversations, and agent actions before they reach users or systems.

> LLMs generate. ControlPlane governs.

## Status

This repository is being built as a demonstrable Round 2 prototype. Demo mode uses deterministic local detectors and seeded data; it does not claim perfect safety or production telemetry.

## Architecture

- `apps/web`: Next.js, TypeScript, Tailwind, Recharts, and Lucide dashboard
- `apps/api`: FastAPI services, Pydantic contracts, deterministic detectors, policy and risk engines
- PostgreSQL and Redis: persistence and cache/job infrastructure for the Docker demo
- `data`: synthetic interactions and knowledge-base fixtures

See `docs/architecture.md` for the control flow and `docs/risk-engine.md` for scoring.

## Run locally

1. Copy `.env.example` to `.env`. Demo mode is enabled by default and needs no external LLM credentials.
2. Start the API: `cd apps/api && python -m venv .venv && .venv\\Scripts\\activate && pip install -e . && uvicorn app.main:app --reload --port 8000`
3. Start the web app in another terminal: `cd apps/web && npm install && npm run dev`
4. Open `http://localhost:3000`. API docs are at `http://localhost:8000/docs`.

Or run `docker compose up --build` for the full local stack.

## Demo behavior

The dashboard labels synthetic activity as demo data. The evaluation API runs deterministic local PII, prompt-injection, grounding-overlap, and simple bias heuristic checks; no LLM call is made in demo mode. The risk engine applies use-case weights, policy thresholds, and safety floors for PII/injection signals. A reviewer can override a decision through `/v1/reviews`; the override remains attached to the audit event and is counted in analytics.

## Demo scenarios

Use `POST /v1/evaluate` with `application` set to `support`, `knowledge`, or `financial`. The financial policy requires grounding for unsupported claims and routes them to review. Pass a stable `conversation_id` to demonstrate prior-turn risk influencing later evaluations. These are deterministic demonstration controls, not a claim of production-grade detection or calibrated model safety.

## Limitations and roadmap

The current prototype uses in-memory demo repositories and deterministic evidence fixtures. Production hardening would add Alembic migrations, tenant authentication, durable event storage, vector retrieval, calibrated ML models, provider adapters, and operational SLOs.
