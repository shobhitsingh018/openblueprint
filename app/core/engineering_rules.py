from typing import Any
from app.core.validation import ValidationResult


def rule_requirements_present(design: dict[str, Any]) -> ValidationResult | None:
    if design.get("requirements"):
        return ValidationResult("DESIGN-002", "INFO", "PASS", "Design contains requirements.")
    return ValidationResult("DESIGN-002", "ERROR", "ERROR", "Design contains no requirements.",
                            suggestion="Define at least one engineering requirement.")


def rule_unique_ids(design: dict[str, Any]) -> ValidationResult | None:
    objects: list[tuple[str, str]] = []
    for collection in ("requirements", "systems", "components", "connections", "constraints", "resources"):
        for item in design.get(collection, []):
            objects.append((collection, str(item.get("id", ""))))
            if collection == "components":
                objects.extend(("interfaces", str(i.get("id", ""))) for i in item.get("interfaces", []))
    missing = [f"{kind}:{item_id or '<missing>'}" for kind, item_id in objects if not item_id]
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for kind, item_id in objects:
        if item_id and item_id in seen:
            duplicates.append(f"{seen[item_id]} and {kind}:{item_id}")
        elif item_id:
            seen[item_id] = f"{kind}:{item_id}"
    if missing or duplicates:
        return ValidationResult("DESIGN-003", "ERROR", "ERROR",
                                "Design contains missing or duplicate IDs.",
                                missing + duplicates,
                                "Assign a non-empty unique ID to every design object.")
    return ValidationResult("DESIGN-003", "INFO", "PASS", "All design object IDs are present and unique.")


def rule_connections_reference_endpoints(design: dict[str, Any]) -> ValidationResult | None:
    known = {i.get("id") for c in design.get("components", []) for i in c.get("interfaces", []) if i.get("id")}
    connections = design.get("connections", [])
    if not connections:
        return None

    problems: list[str] = []
    for c in connections:
        cid = c.get("id", "unknown")
        src = c.get("source")
        tgt = c.get("target")
        if src not in known:
            problems.append(f"{cid}.source='{src}' (not a defined interface)")
        if tgt not in known:
            problems.append(f"{cid}.target='{tgt}' (not a defined interface)")

    if problems:
        return ValidationResult(
            "CONNECTION-003", "ERROR", "ERROR",
            "One or more connections reference unknown interfaces.",
            problems,
            "Ensure connection endpoints reference defined interface IDs. "
            f"Known interfaces: {sorted(known) if known else '[]'}",
        )
    return ValidationResult("CONNECTION-003", "INFO", "PASS", "All connection endpoints reference defined interfaces.")


def rule_components_have_interfaces(design: dict[str, Any]) -> ValidationResult | None:
    components = design.get("components", [])
    if not components:
        return None
    missing = [c.get("id", "unknown") for c in components if not c.get("interfaces")]
    if missing:
        return ValidationResult("COMPONENT-002", "WARNING", "INCOMPLETE",
                                "One or more components have no interfaces.", missing,
                                "Define the interfaces needed for power, data, control, or mechanical integration.")
    return ValidationResult("COMPONENT-002", "INFO", "PASS", "All components have at least one interface.")


def rule_system_component_references(design: dict[str, Any]) -> ValidationResult | None:
    systems = design.get("systems", [])
    component_ids = {c.get("id") for c in design.get("components", [])}
    if not systems or not component_ids:
        return None
    unresolved = []
    for s in systems:
        for cid in s.get("component_ids", []):
            if cid not in component_ids:
                unresolved.append(f"{s.get('id', 'unknown')}->{cid}")
    if unresolved:
        return ValidationResult("SYSTEM-002", "ERROR", "ERROR",
                                "A system references an unknown component.", unresolved,
                                "Reference only defined component IDs from system.component_ids.")
    return ValidationResult("SYSTEM-002", "INFO", "PASS", "System component references are valid.")


def rule_design_completeness(design: dict[str, Any]) -> ValidationResult | None:
    missing: list[str] = []
    if not design.get("systems"): missing.append("systems")
    if not design.get("components"): missing.append("components")
    components = design.get("components", [])
    if components and any(not c.get("interfaces") for c in components): missing.append("interfaces")
    if components and design.get("systems") and not design.get("connections"): missing.append("connections")
    if missing:
        return ValidationResult("DESIGN-004", "WARNING", "INCOMPLETE",
                                "Design is structurally incomplete for an engineering first pass.",
                                sorted(set(missing)),
                                "Complete the missing architecture elements before treating the design as ready.")
    return ValidationResult("DESIGN-004", "INFO", "PASS", "Design contains the expected first-pass architecture elements.")


def assess_design_status(results: list[dict[str, Any]]) -> str:
    if any(r["status"] == "ERROR" for r in results): return "INVALID"
    if any(r["status"] == "INCOMPLETE" for r in results): return "INCOMPLETE"
    return "VALID"