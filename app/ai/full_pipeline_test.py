import os
import sys
from app.ai.config import AIConfig
from app.ai.converter import proposal_to_design
from app.ai.health import check_model_available
from app.ai.request import DesignRequest
from app.ai.service import generate_design_proposal
from app.core.engineering_rules import assess_design_status
from app.core.validate_design import validate_design


def main() -> int:
    base_url = os.getenv("OPENBLUEPRINT_OLLAMA_URL", "http://127.0.0.1:11434")
    model = os.getenv("OPENBLUEPRINT_MODEL", "qwen2.5:3b-instruct")

    # Fail fast with an actionable message instead of a raw connection
    # traceback if Ollama isn't reachable or the model isn't pulled.
    check = check_model_available(model, base_url)
    if not check["ready"]:
        print("=== OLLAMA PREFLIGHT CHECK FAILED ===")
        print(check["message"])
        return 1

    request = DesignRequest(
        prompt="Design a temperature monitoring system using a microcontroller, temperature sensor, local display, and 5V power supply.",
        domain="embedded electronics",
    )

    try:
        proposal = generate_design_proposal(
            request, AIConfig(provider="ollama", model=model, refinement_passes=1)
        )
    except (RuntimeError, ValueError) as exc:
        # Raised by OllamaProvider with a specific, actionable diagnosis.
        print("=== PIPELINE FAILED ===")
        print(str(exc))
        return 1

    design = proposal_to_design(proposal, "qwen-test-001", "Temperature Monitoring System")
    results = validate_design(design)
    status = assess_design_status(results)
    print("=== MODEL ===\n", model)
    print("=== PROPOSAL ===")
    print(proposal.model_dump_json(indent=2))
    print("\n=== DESIGN ===")
    print(design.model_dump_json(indent=2))
    print(f"\n=== READINESS: {status} ===")
    print("\n=== VALIDATION ===")
    for result in results:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
