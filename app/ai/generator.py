from app.ai.parser import parse_proposal
from app.ai.prompt import build_engineering_prompt
from app.ai.proposal import DesignProposal
from app.ai.provider import AIProvider
from app.ai.request import DesignRequest


def generate_proposal(request: DesignRequest, provider: AIProvider) -> DesignProposal:
    schema = DesignProposal.model_json_schema()
    raw = provider.generate(build_engineering_prompt(request), response_schema=schema)
    return parse_proposal(raw)
