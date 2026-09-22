from app.ai.proposal import DesignProposal
from app.core.design import Design


def proposal_to_design(
    proposal: DesignProposal,
    design_id: str,
    name: str,
) -> Design:

    return Design(
        id=design_id,
        name=name,
        description=proposal.summary,
        requirements=proposal.requirements,
        systems=proposal.systems,
        components=proposal.components,
        connections=proposal.connections,
        constraints=proposal.constraints,
        resources=proposal.resources,
        metadata={
            "assumptions": proposal.assumptions,
            "warnings": proposal.warnings,
            "source": "ai_proposal",
        },
    )
