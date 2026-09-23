from app.core.validation import ValidationResult


def rule_interface_ids_required(design: dict) -> ValidationResult | None:
    interfaces = [i for c in design.get("components", []) for i in c.get("interfaces", [])]
    if not interfaces:
        return ValidationResult("INTERFACE-001", "WARNING", "WARNING",
                                "Design does not contain any interfaces yet.",
                                suggestion="Define interfaces for components so connections can be validated.")
    missing = [str(i.get("name", "Unnamed interface")) for i in interfaces if not i.get("id")]
    if missing:
        return ValidationResult("INTERFACE-001", "ERROR", "ERROR",
                                "One or more interfaces are missing an ID.", missing,
                                "Assign a unique ID to every interface.")
    return ValidationResult("INTERFACE-001", "INFO", "PASS", "All interfaces have valid IDs.")
