import json
from app.ai.proposal import DesignProposal, ProposalComponent, ProposalInterface, ProposalRequirement, ProposalSystem, ProposalConnection
from app.ai.provider import AIProvider


class MockProvider(AIProvider):
    def generate(self, prompt: str, response_schema=None) -> str:
        proposal = DesignProposal(
            summary="Mock complete first-pass architecture.",
            requirements=[ProposalRequirement(id="req-001", type="functional", description="Provide the requested engineering function.")],
            systems=[ProposalSystem(id="sys-001", name="Main System", component_ids=["comp-001", "comp-002"])],
            components=[
                ProposalComponent(id="comp-001", name="Controller", category="compute",
                                  interfaces=[ProposalInterface(id="if-001", name="Data Out", type="data", direction="output")]),
                ProposalComponent(id="comp-002", name="Sensor", category="sensor",
                                  interfaces=[ProposalInterface(id="if-002", name="Data In", type="data", direction="input")]),
            ],
            connections=[ProposalConnection(id="conn-001", name="Sensor data", source="if-002", target="if-001", interface_type="data")],
            assumptions=["Mock provider output is for pipeline tests only."],
        )
        return json.dumps(proposal.model_dump())
