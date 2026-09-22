from typing import Any

from app.core.validation import ValidationResult


def rule_interface_ids_required(
    design: dict[str, Any],
) -> ValidationResult | None:

    interfaces = []

    for component in design.get("components", []):
        interfaces.extend(component.get("interfaces", []))

    if not interfaces:
        return ValidationResult(
            rule_id="INTERFACE-001",
            severity="WARNING",
            status="WARNING",
            message="Design does not contain any interfaces yet.",
            suggestion="Define interfaces for components so connections can be validated.",
        )

    missing_ids = [
        str(interface.get("name", "Unnamed interface"))
        for interface in interfaces
        if not interface.get("id")
    ]

    if missing_ids:
        return ValidationResult(
            rule_id="INTERFACE-001",
            severity="ERROR",
            status="ERROR",
            message="One or more interfaces are missing an ID.",
            affected_objects=missing_ids,
            suggestion="Assign a unique ID to every interface.",
        )

    return ValidationResult(
        rule_id="INTERFACE-001",
        severity="INFO",
        status="PASS",
        message="All interfaces have valid IDs.",
    )
