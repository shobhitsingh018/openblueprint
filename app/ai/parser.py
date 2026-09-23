import json

from app.ai.proposal import DesignProposal


def parse_proposal(response: str) -> DesignProposal:
    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError("AI response is not valid JSON.") from exc

    if not isinstance(data, dict):
        raise ValueError("AI response must be a JSON object.")

    try:
        return DesignProposal.model_validate(data)
    except Exception as exc:
        raise ValueError("AI response does not match the DesignProposal schema.") from exc
