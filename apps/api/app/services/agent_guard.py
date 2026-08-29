from app.schemas.action import ActionRequest, ActionResponse
from app.schemas.evaluation import Decision

ACTION_RISK = {"READ_DOCUMENT": (12, Decision.ALLOW), "SEARCH_DATABASE": (28, Decision.ALLOW), "SEND_EMAIL": (55, Decision.HUMAN_REVIEW), "CREATE_TICKET": (35, Decision.ALLOW), "DELETE_RECORD": (88, Decision.BLOCK), "TRANSFER_FUNDS": (96, Decision.HUMAN_REVIEW)}


def evaluate_action(request: ActionRequest) -> ActionResponse:
    risk, decision = ACTION_RISK.get(request.action.upper(), (72, Decision.HUMAN_REVIEW))
    reason = "High-impact action requires human approval" if decision == Decision.HUMAN_REVIEW else "Action is within the configured agent policy"
    if request.action.upper() == "DELETE_RECORD":
        reason = "Destructive action is blocked by default"
    return ActionResponse(decision=decision, risk_score=risk, reason=reason)
