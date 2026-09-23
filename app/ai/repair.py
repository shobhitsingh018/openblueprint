"""Structural guardrails for model proposals.

OpenBlueprint must never silently guess which interface a malformed connection
was intended to use. Connection references are therefore validated rather than
rewired. Interface synthesis is also avoided here; architecture stages must
explicitly define functional interfaces.
"""

from app.ai.proposal import DesignProposal


def repair_proposal(proposal: DesignProposal) -> DesignProposal:
    known_interfaces = {i.id for c in proposal.components for i in c.interfaces}
    invalid = []
    for conn in proposal.connections:
        for endpoint in (conn.source, conn.target):
            if endpoint not in known_interfaces:
                invalid.append(f"{conn.id}:{endpoint}")
    if invalid:
        raise ValueError(
            "Proposal contains invalid connection endpoints; refusing to guess or rewire them: "
            + ", ".join(invalid)
        )
    return proposal
