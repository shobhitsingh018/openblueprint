from typing import Any

from app.core.validation import ValidationResult


def rule_system_ids_required(
    design: dict[str, Any],
) -> ValidationResult | None:

    systems = design.get("systems", [])

    if not systems:
        return ValidationResult(
            rule_id="SYSTEM-001",
            severity="WARNING",
            status="WARNING",
            message="Design does not contain any systems yet.",
            suggestion="Add at least one system or subsystem.",
        )

    missing_ids = [
        str(system.get("name", "Unnamed system"))
        for system in systems
        if not system.get("id")
    ]

    if missing_ids:
        return ValidationResult(
            rule_id="SYSTEM-001",
            severity="ERROR",
            status="ERROR",
            message="One or more systems are missing an ID.",
            affected_objects=missing_ids,
            suggestion="Assign a unique ID to every system.",
        )

    return ValidationResult(
        rule_id="SYSTEM-001",
        severity="INFO",
        status="PASS",
        message="All systems have valid IDs.",
    )
