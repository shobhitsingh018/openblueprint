from typing import Any

from app.core.validation import ValidationResult


def rule_requirements_present(
    design: dict[str, Any],
) -> ValidationResult | None:

    if not design.get("requirements"):
        return ValidationResult(
            rule_id="DESIGN-002",
            severity="ERROR",
            status="ERROR",
            message="Design contains no requirements.",
            suggestion="Define at least one engineering requirement.",
        )

    return ValidationResult(
        rule_id="DESIGN-002",
        severity="INFO",
        status="PASS",
        message="Design contains requirements.",
    )


def rule_connections_reference_endpoints(
    design: dict[str, Any],
) -> ValidationResult | None:

    components = design.get("components", [])

    known_interfaces = set()

    for component in components:
        for interface in component.get("interfaces", []):
            known_interfaces.add(interface.get("id"))

    connections = design.get("connections", [])

    if not connections:
        return None

    unresolved = []

    for connection in connections:
        source = connection.get("source")
        target = connection.get("target")

        if source not in known_interfaces or target not in known_interfaces:
            unresolved.append(connection.get("id", "unknown"))

    if unresolved:
        return ValidationResult(
            rule_id="CONNECTION-003",
            severity="ERROR",
            status="ERROR",
            message="One or more connections reference unknown interfaces.",
            affected_objects=unresolved,
            suggestion="Ensure connection endpoints reference defined interfaces.",
        )

    return ValidationResult(
        rule_id="CONNECTION-003",
        severity="INFO",
        status="PASS",
        message="All connection endpoints reference defined interfaces.",
    )
