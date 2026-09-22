from app.core.design import Design
from app.core.validation import (
    ValidationEngine,
    rule_design_name_required,
)
from app.core.system_rules import rule_system_ids_required
from app.core.component_rules import rule_component_ids_required
from app.core.interface_rules import rule_interface_ids_required
from app.core.connection_rules import rule_connection_ids_required
from app.core.connection_endpoint_rules import rule_connection_endpoints_required


def validate_design(design: Design) -> list[dict]:
    engine = ValidationEngine()

    engine.register_rule(rule_design_name_required)
    engine.register_rule(rule_system_ids_required)
    engine.register_rule(rule_component_ids_required)
    engine.register_rule(rule_interface_ids_required)
    engine.register_rule(rule_connection_ids_required)
    engine.register_rule(rule_connection_endpoints_required)

    return engine.validate(design.model_dump())


if __name__ == "__main__":
    design = Design(
        id="demo-001",
        name="Smart Environmental Monitor",
        systems=[
            {
                "id": "sys-001",
                "name": "Sensing System",
            }
        ],
        components=[
            {
                "id": "comp-001",
                "name": "Temperature Sensor",
                "interfaces": [
                    {
                        "id": "if-001",
                        "name": "I2C",
                    }
                ],
            }
        ],
        connections=[
            {
                "id": "conn-001",
                "name": "Sensor to Controller",
                "source": "sensor-i2c",
                "target": "controller-i2c",
            }
        ],
    )

    results = validate_design(design)

    for result in results:
        print(result)
