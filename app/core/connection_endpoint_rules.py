from typing import Any

from app.core.validation import ValidationResult


def rule_connection_endpoints_required(
    design: dict[str, Any],
) -> ValidationResult | None:

    connections = design.get("connections", [])

    if not connections:
        return None

    invalid_connections = []

    for connection in connections:
        connection_name = connection.get(
            "name",
            connection.get("id", "Unnamed connection")
        )

        if not connection.get("source") or not connection.get("target"):
            invalid_connections.append(str(connection_name))

    if invalid_connections:
        return ValidationResult(
            rule_id="CONNECTION-002",
            severity="ERROR",
            status="ERROR",
            message="One or more connections are missing a source or target endpoint.",
            affected_objects=invalid_connections,
            suggestion="Define both source and target endpoints for every connection.",
        )

    return ValidationResult(
        rule_id="CONNECTION-002",
        severity="INFO",
        status="PASS",
        message="All connections have valid source and target endpoints.",
    )
