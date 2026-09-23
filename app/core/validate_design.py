from app.core.component_rules import rule_component_ids_required
from app.core.connection_endpoint_rules import rule_connection_endpoints_required
from app.core.connection_rules import rule_connection_ids_required
from app.core.design import Design
from app.core.engineering_rules import (
    rule_components_have_interfaces,
    rule_connections_reference_endpoints,
    rule_design_completeness,
    rule_requirements_present,
    rule_system_component_references,
    rule_unique_ids,
)
from app.core.interface_rules import rule_interface_ids_required
from app.core.system_rules import rule_system_ids_required
from app.core.validation import ValidationEngine, rule_design_name_required


def validate_design(design: Design) -> list[dict]:
    engine = ValidationEngine()
    for rule in (
        rule_design_name_required,
        rule_requirements_present,
        rule_unique_ids,
        rule_system_ids_required,
        rule_system_component_references,
        rule_component_ids_required,
        rule_components_have_interfaces,
        rule_interface_ids_required,
        rule_connection_ids_required,
        rule_connection_endpoints_required,
        rule_connections_reference_endpoints,
        rule_design_completeness,
    ):
        engine.register_rule(rule)
    return engine.validate(design.model_dump())
