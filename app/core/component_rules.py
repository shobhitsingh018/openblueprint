from typing import Any
from app.core.validation import ValidationResult


def rule_component_ids_required(design: dict[str, Any]) -> ValidationResult | None:
    components = design.get("components", [])
    if not components:
        return ValidationResult("COMPONENT-001", "WARNING", "WARNING",
                                "Design does not contain any components yet.",
                                suggestion="Add components to the design.")
    missing = [str(c.get("name", "Unnamed component")) for c in components if not c.get("id")]
    if missing:
        return ValidationResult("COMPONENT-001", "ERROR", "ERROR",
                                "One or more components are missing an ID.", missing,
                                "Assign a unique ID to every component.")
    return ValidationResult("COMPONENT-001", "INFO", "PASS", "All components have valid IDs.")
