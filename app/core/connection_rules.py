from app.core.validation import ValidationResult


def rule_connection_ids_required(design: dict) -> ValidationResult | None:
    connections = design.get("connections", [])
    if not connections:
        return ValidationResult("CONNECTION-001", "WARNING", "WARNING",
                                "Design does not contain any connections yet.",
                                suggestion="Define connections between system elements.")
    missing = [str(c.get("name", "Unnamed connection")) for c in connections if not c.get("id")]
    if missing:
        return ValidationResult("CONNECTION-001", "ERROR", "ERROR",
                                "One or more connections are missing an ID.", missing,
                                "Assign a unique ID to every connection.")
    return ValidationResult("CONNECTION-001", "INFO", "PASS", "All connections have valid IDs.")
