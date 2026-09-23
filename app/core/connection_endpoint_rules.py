from app.core.validation import ValidationResult


def rule_connection_endpoints_required(design: dict) -> ValidationResult | None:
    connections = design.get("connections", [])
    if not connections:
        return None
    invalid = [str(c.get("id", c.get("name", "unknown"))) for c in connections
               if not c.get("source") or not c.get("target")]
    if invalid:
        return ValidationResult("CONNECTION-002", "ERROR", "ERROR",
                                "One or more connections are missing a source or target endpoint.", invalid,
                                "Define both source and target interface IDs for every connection.")
    return ValidationResult("CONNECTION-002", "INFO", "PASS", "All connections have source and target endpoints.")
