from app.ai.models import MODEL_PROFILES
from app.ai.request import DesignRequest
from app.ai.router import RoutingDecision, route_task


def select_model(
    request: DesignRequest,
) -> tuple[RoutingDecision, str]:

    decision = route_task(
        request.prompt,
        request.task_type,
    )

    for profile in MODEL_PROFILES.values():
        if decision.role in profile.roles:
            return decision, profile.name

    raise ValueError(
        f"No model configured for role: {decision.role}"
    )
