"""AI-driven repair of invalid design proposals."""

from __future__ import annotations
from typing import Any, Callable

from app.ai.prompt import build_repair_prompt
from app.ai.normalize import normalize_proposal


def repair_proposal(
    raw: dict,
    errors: list[str],
    call_model: Callable[[str], str],
    parse_json: Callable[[str], dict],
    max_attempts: int = 2,
) -> dict:
    """Feed validation errors back to the model until clean or exhausted."""
    current = raw
    for attempt in range(max_attempts):
        if not errors:
            break
        prompt = build_repair_prompt(
            raw_json=__import__("json").dumps(current, indent=2),
            errors=errors,
        )
        try:
            response = call_model(prompt)
            parsed = parse_json(response)
            current = normalize_proposal(parsed)
        except Exception:
            break
    return current