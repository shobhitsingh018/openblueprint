import json

from app.ai.provider import AIProvider
from app.ai.proposal import DesignProposal


class MockProvider(AIProvider):

    def generate(self, prompt: str) -> str:
        proposal = DesignProposal(
            summary=f"Generated proposal for: {prompt}",
            requirements=[
                {
                    "id": "req-001",
                    "type": "functional",
                    "description": prompt,
                }
            ],
            assumptions=[
                "Detailed component selection requires engineering constraints."
            ],
        )

        return json.dumps(proposal.model_dump())
