"""End-to-end pipeline test: prompt -> AI -> normalize -> validate -> repair."""

import json
from typing import Any

from pydantic import ValidationError

from app.ai.prompt import build_design_prompt
from app.ai.normalize import normalize_proposal
from app.ai.repair import repair_proposal
from app.core.validate_design import validate_design
from app.ai.converter import proposal_to_design
from app.ai.proposal import DesignProposal


def _status(r: Any) -> str:
    return r["status"] if isinstance(r, dict) else getattr(r, "status", "")


def _message(r: Any) -> str:
    return r["message"] if isinstance(r, dict) else getattr(r, "message", str(r))


def _try_convert(raw: dict):
    """Attempt Pydantic validation + conversion.

    Returns (design, results, errors).
    On ValidationError, design/results are None and errors is a list of strings.
    """
    try:
        proposal = DesignProposal.model_validate(raw)
    except ValidationError as exc:
        error_strings = []
        for err in exc.errors():
            loc = ".".join(str(p) for p in err.get("loc", []))
            error_strings.append(f"{loc}: {err.get('msg', 'invalid')}")
        return None, None, error_strings

    design = proposal_to_design(
        proposal, design_id="DESIGN-1", name="Generated Design"
    )
    results = validate_design(design)
    errors = [r for r in results if _status(r) == "ERROR"]
    return design, results, errors


def run_full_pipeline(description: str, provider, refinement_passes: int = 2):
    # 1. Generate
    prompt = build_design_prompt(description)
    schema = DesignProposal.model_json_schema()
    try:
        response = provider.generate(prompt, response_schema=schema)
    except TypeError:
        response = provider.generate(prompt)
    raw = json.loads(response)

    # 2. Normalize
    raw = normalize_proposal(raw)

    # 3. Convert + validate
    design, results, errors = _try_convert(raw)
    print(f"[pipeline] initial errors: {len(errors)}")

    # 4. Repair loop
    for attempt in range(1, refinement_passes + 1):
        if not errors:
            break
        print(f"[repair] attempt {attempt}: {len(errors)} error(s)")
        for e in errors:
            print(f"         - {_message(e) if not isinstance(e, str) else e}")

        raw = repair_proposal(
            raw,
            [e if isinstance(e, str) else _message(e) for e in errors],
            call_model=provider.generate,
            parse_json=json.loads,
        )
        raw = normalize_proposal(raw)  # re-sanitize after repair
        design, results, errors = _try_convert(raw)

    if results is None:
        # Never got a valid DesignProposal
        print("[pipeline] failed to produce a valid DesignProposal after repair")
        return None, []

    return design, results


def _print_report(results):
    print("\n=== VALIDATION REPORT ===")
    for r in results:
        status = _status(r)
        msg = _message(r)
        marker = {
            "PASS": "OK ",
            "INFO": "OK ",
            "WARNING": "!! ",
            "INCOMPLETE": "~~ ",
            "ERROR": "XX ",
        }.get(status, "?  ")
        print(f"  {marker}[{status}] {msg}")
    print("=========================\n")


if __name__ == "__main__":
    description = "Design a simple temperature monitoring system with a sensor and a display."

    # --- STEP 1: mock provider (no AI) ---
    from app.ai.mock_provider import MockProvider
    print("Running with MockProvider...")
    _, mock_results = run_full_pipeline(description, MockProvider())
    _print_report(mock_results)

    # --- STEP 2: real provider ---
    from app.ai.ollama_provider import OllamaProvider
    print("Running with OllamaProvider...")
    _, real_results = run_full_pipeline(description, OllamaProvider())
    _print_report(real_results)