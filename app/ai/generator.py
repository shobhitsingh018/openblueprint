from app.ai.request import DesignRequest
from app.ai.proposal import DesignProposal


def generate_proposal(request: DesignRequest) -> DesignProposal:
    return DesignProposal(
        summary=f"Engineering design proposal for: {request.prompt}",
        requirements=[
            {
                "id": "req-001",
                "type": "functional",
                "description": request.prompt,
            }
        ],
        assumptions=[
            "The requested system should be designed as a modular engineering system.",
            "Specific component selection requires additional engineering constraints.",
        ],
        warnings=[
            "This is a preliminary proposal and has not been validated against physical requirements."
        ],
    )
