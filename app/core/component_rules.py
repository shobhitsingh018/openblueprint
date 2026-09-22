from typing import Any

from app.core.validation import ValidationResult


def rule_component_ids_required(
    design: dict[str, Any],
) -> ValidationResult | None:

    components = design.get("components", [])

    if not components:
        return ValidationResult(
            rule_id="COMPONENT-001",
            severity="WARNING",
            status="WARNING",
            message="Design does not contain any components yet.",
            suggestion="Add components to the design.",
        )

    missing_ids = [
        str(component.get("name", "Unnamed component"))
        for component in components
        if not component.get("id")
    ]

    if missing_ids:
        return ValidationResult(
            rule_id="COMPONENT-001",
            severity="ERROR",
            status="ERROR",
            message="One or more components are missing an ID.",
            affected_objects=missing_ids,
            suggestion="Assign a unique ID to every component.",
        )

    return ValidationResult(
        rule_id="COMPONENT-001",
        severity="INFO",
        status="PASS",
        message="All components have valid IDs.",
    )
