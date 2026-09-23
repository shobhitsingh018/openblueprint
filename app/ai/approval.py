from app.ai.proposal import DesignProposal


def approve_proposal(proposal: DesignProposal) -> DesignProposal:
    if proposal.status != "PROPOSED":
        raise ValueError(f"Only PROPOSED designs can be approved. Current status: {proposal.status}")
    proposal.status = "APPROVED"
    return proposal


def reject_proposal(proposal: DesignProposal) -> DesignProposal:
    if proposal.status != "PROPOSED":
        raise ValueError(f"Only PROPOSED designs can be rejected. Current status: {proposal.status}")
    proposal.status = "REJECTED"
    return proposal
