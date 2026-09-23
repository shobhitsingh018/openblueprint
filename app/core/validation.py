from typing import Any, Callable


class ValidationResult:
    def __init__(self, rule_id: str, severity: str, status: str, message: str,
                 affected_objects: list[str] | None = None, suggestion: str = ""):
        self.rule_id = rule_id
        self.severity = severity
        self.status = status
        self.message = message
        self.affected_objects = affected_objects or []
        self.suggestion = suggestion

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id, "severity": self.severity, "status": self.status,
            "message": self.message, "affected_objects": self.affected_objects,
            "suggestion": self.suggestion,
        }


Rule = Callable[[dict[str, Any]], ValidationResult | None]


class ValidationEngine:
    def __init__(self) -> None:
        self.rules: list[Rule] = []

    def register_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def validate(self, design: dict[str, Any]) -> list[dict[str, Any]]:
        return [result.to_dict() for rule in self.rules if (result := rule(design)) is not None]


def rule_design_name_required(design: dict[str, Any]) -> ValidationResult | None:
    name = str(design.get("name", "")).strip()
    if name:
        return ValidationResult("DESIGN-001", "INFO", "PASS", "Design has a valid name.")
    return ValidationResult("DESIGN-001", "ERROR", "ERROR", "Design name is missing.",
                            suggestion="Provide a name for the design.")
