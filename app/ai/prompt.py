"""Prompts for the legacy single-shot proposal path."""

SYSTEM_PROMPT = """
You are OpenBlueprint's preliminary engineering architecture engine. Return one JSON object only.
OpenBlueprint is domain-independent. Propose a structurally complete first-pass architecture.
Never invent manufacturers, part numbers, datasheets, certifications, tests, simulations, or precise
engineering limits that the user did not provide. Unknown values are null and zero is a real value.
Every functional component needs interfaces. Connection endpoints must be interface IDs.
"""


def build_engineering_prompt(request) -> str:
    return (
        SYSTEM_PROMPT
        + f"\nTASK TYPE: {request.task_type}\nDOMAIN: {request.domain or 'general engineering'}"
        + "\nGOALS:\n- " + "\n- ".join(request.goals or ["Create a complete first-pass architecture."])
        + "\nCONSTRAINTS:\n- " + "\n- ".join(request.constraints or ["None provided."])
        + "\nREQUIRED OUTPUT FIELDS: summary, status, requirements, systems, components, connections, constraints, resources, assumptions, warnings."
        + f"\nUSER REQUIREMENT:\n{request.prompt}\n\nReturn only JSON."
    )


def build_refinement_prompt(request, proposal, missing) -> str:
    return (
        SYSTEM_PROMPT
        + "\nYou are refining an existing proposal. Return the COMPLETE replacement proposal."
        + "\nMissing structural elements: " + ", ".join(missing)
        + "\nORIGINAL REQUIREMENT:\n" + request.prompt
        + "\nCURRENT PROPOSAL:\n" + proposal.model_dump_json(indent=2)
        + "\nPreserve valid information and fix only justified issues. Return only JSON."
    )
