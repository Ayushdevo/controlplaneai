from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.policies.catalog import POLICIES
from app.schemas.action import ActionRequest, ActionResponse
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.schemas.review import ReviewRequest
from uuid import UUID
from app.services.agent_guard import evaluate_action
from app.services.demo_store import store
from app.services.evaluation import EvaluationService

app = FastAPI(title="ControlPlane.ai API", version="0.1.0", description="AI runtime governance and safety control plane")
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in settings.api_cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
evaluation_service = EvaluationService()


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": settings.app_name, "demo_mode": settings.demo_mode}


@app.post("/v1/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    return store.save_evaluation(evaluation_service.evaluate(request))


@app.post("/v1/evaluate/input", response_model=EvaluationResponse)
def evaluate_input(request: EvaluationRequest) -> EvaluationResponse:
    return evaluation_service.evaluate(request.model_copy(update={"output": ""}))


@app.post("/v1/evaluate/output", response_model=EvaluationResponse)
def evaluate_output(request: EvaluationRequest) -> EvaluationResponse:
    return evaluation_service.evaluate(request)


@app.post("/v1/evaluate/action", response_model=ActionResponse)
def evaluate_evaluate_action(request: ActionRequest) -> ActionResponse:
    return evaluate_action(request)


@app.post("/v1/agent/evaluate-action", response_model=ActionResponse)
def evaluate_agent_action(request: ActionRequest) -> ActionResponse:
    return evaluate_action(request)


@app.get("/v1/applications")
def applications() -> list[dict]:
    return [{"id": key, "name": value["name"], "policy": value} for key, value in POLICIES.items()]


@app.get("/v1/policies")
def policies() -> dict:
    return POLICIES


@app.get("/v1/incidents")
def incidents() -> dict:
    items = store.list_incidents()
    return {"items": items, "total": len(items), "demo": settings.demo_mode}


@app.get("/v1/incidents/{audit_id}")
def incident(audit_id: UUID) -> EvaluationResponse:
    from fastapi import HTTPException
    evaluation = store.get_evaluation(audit_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return evaluation


@app.get("/v1/audit")
def audit() -> dict:
    items = list(store.evaluations.values())
    return {"items": items, "total": len(items), "demo": settings.demo_mode}


@app.post("/v1/reviews")
def review(request: ReviewRequest) -> dict:
    from fastapi import HTTPException
    evaluation = store.get_evaluation(request.audit_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return store.add_review(request, evaluation.decision).model_dump(mode="json")


@app.get("/v1/analytics")
def analytics() -> dict:
    return store.analytics()
