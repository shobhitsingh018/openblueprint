from typing import Any, Callable


class ValidationResult:
    def __init__(
        self,
        rule_id: str,
        severity: str,
        status: str,
        message: str,
        affected_objects: list[str] | None = None,
        suggestion: str = "",
    ):
        self.rule_id = rule_id
        self.severity = severity
        self.status = status
        self.message = message
        self.affected_objects = affected_objects or []
        self.suggestion = suggestion

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "status": self.status,
            "message": self.message,
            "affected_objects": self.affected_objects,
            "suggestion": self.suggestion,
        }


class ValidationEngine:
    def __init__(self):
        self.rules: list[Callable[[dict[str, Any]], ValidationResult | None]] = []

    def register_rule(
        self,
        rule: Callable[[dict[str, Any]], ValidationResult | None],
    ) -> None:
        self.rules.append(rule)

    def validate(self, design: dict[str, Any]) -> list[dict[str, Any]]:
        results = []

        for rule in self.rules:
            result = rule(design)

            if result is not None:
                results.append(result.to_dict())

        return results


def rule_design_name_required(
    design: dict[str, Any],
) -> ValidationResult | None:
    name = design.get("name", "").strip()

    if name:
        return ValidationResult(
            rule_id="DESIGN-001",
            severity="INFO",
            status="PASS",
            message="Design has a valid name.",
        )

    return ValidationResult(
        rule_id="DESIGN-001",
        severity="ERROR",
        status="ERROR",
        message="Design name is missing.",
        suggestion="Provide a name for the design.",
    )
