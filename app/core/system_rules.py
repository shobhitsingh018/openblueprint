from typing import Any
from app.core.validation import ValidationResult


def rule_system_ids_required(design: dict[str, Any]) -> ValidationResult | None:
    systems = design.get("systems", [])
    if not systems:
        return ValidationResult("SYSTEM-001", "WARNING", "WARNING",
                                "Design does not contain any systems yet.",
                                suggestion="Add at least one system or subsystem.")
    missing = [str(s.get("name", "Unnamed system")) for s in systems if not s.get("id")]
    if missing:
        return ValidationResult("SYSTEM-001", "ERROR", "ERROR",
                                "One or more systems are missing an ID.", missing,
                                "Assign a unique ID to every system.")
    return ValidationResult("SYSTEM-001", "INFO", "PASS", "All systems have valid IDs.")
