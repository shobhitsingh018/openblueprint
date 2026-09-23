from app.ai.config import AIConfig
from app.ai.converter import proposal_to_design
from app.ai.factory import create_provider
from app.ai.models import MODEL_PROFILES
from app.ai.proposal import DesignProposal
from app.ai.request import DesignRequest
from app.ai.router import route_task
from app.core.engineering_rules import assess_design_status
from app.core.validate_design import validate_design


def _missing_elements(proposal: DesignProposal) -> list[str]:
    design = proposal_to_design(proposal, "quality-check", proposal.summary or "Proposed Design")
    results = validate_design(design)
    # Structural problems come back from the validator with two different
    # severities: "INCOMPLETE" (e.g. a component with no interfaces yet) and
    # "ERROR" (e.g. a connection pointing at an interface ID that doesn't
    # exist, or a system referencing a component that was never defined).
    # Both are things a refinement pass can actually fix, so both must be
    # surfaced here - filtering to INCOMPLETE only silently skips the most
    # severe class of problem and lets broken references reach the final
    # proposal unrepaired even when refinement_passes > 0.
    issues: list[str] = []
    for r in results:
        if r["status"] not in ("ERROR", "INCOMPLETE"):
            continue
        objects = ", ".join(r["affected_objects"])
        issues.append(f"{r['message']} Affected: {objects}" if objects else r["message"])
    return sorted(set(issues))


def generate_design_proposal(request: DesignRequest, config: AIConfig) -> DesignProposal:
    if config.provider == "ollama" and not config.model:
        decision = route_task(request.prompt, request.task_type)
        profile = next((p for p in MODEL_PROFILES.values() if decision.role in p.roles), None)
        if profile is None:
            raise ValueError(f"No model configured for role: {decision.role}")
        config = config.model_copy(update={"model": profile.name})

    provider = create_provider(config)
    if config.provider == "ollama":
        from app.ai.staged_pipeline import generate_staged_proposal
        return generate_staged_proposal(request, provider)

    from app.ai.generator import generate_proposal
    return generate_proposal(request, provider)


def assess_proposal(proposal: DesignProposal) -> dict:
    design = proposal_to_design(proposal, "assessment", proposal.summary or "Proposed Design")
    results = validate_design(design)
    return {"status": assess_design_status(results), "results": results}
