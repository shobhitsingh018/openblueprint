from app.ai.config import AIConfig
from app.ai.factory import create_provider
from app.ai.parser import parse_proposal
from app.ai.proposal import DesignProposal
from app.ai.request import DesignRequest


def generate_design_proposal(
    request: DesignRequest,
    config: AIConfig,
) -> DesignProposal:

    provider = create_provider(config)

    response = provider.generate(request.prompt)

    return parse_proposal(response)
