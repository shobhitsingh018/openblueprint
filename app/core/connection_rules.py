from typing import Any

from app.core.validation import ValidationResult


def rule_connection_ids_required(
    design: dict[str, Any],
) -> ValidationResult | None:

    connections = design.get("connections", [])

    if not connections:
        return ValidationResult(
            rule_id="CONNECTION-001",
            severity="WARNING",
            status="WARNING",
            message="Design does not contain any connections yet.",
            suggestion="Define connections between system elements.",
        )

    missing_ids = [
        str(connection.get("name", "Unnamed connection"))
        for connection in connections
        if not connection.get("id")
    ]

    if missing_ids:
        return ValidationResult(
            rule_id="CONNECTION-001",
            severity="ERROR",
            status="ERROR",
            message="One or more connections are missing an ID.",
            affected_objects=missing_ids,
            suggestion="Assign a unique ID to every connection.",
        )

    return ValidationResult(
        rule_id="CONNECTION-001",
        severity="INFO",
        status="PASS",
        message="All connections have valid IDs.",
    )
