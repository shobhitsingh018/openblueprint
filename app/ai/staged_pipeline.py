from __future__ import annotations

import json

from app.ai.parser import parse_proposal
from app.ai.proposal import (
    DesignProposal,
    ProposalComponent,
    ProposalConnection,
    ProposalInterface,
    ProposalRequirement,
    ProposalSystem,
)
from app.ai.provider import AIProvider
from app.ai.request import DesignRequest
from app.ai.staged_models import ArchitectureStage, ConnectionStage


ARCHITECTURE_PROMPT = """
You are OpenBlueprint's architecture decomposition engine.
Return ONE JSON object and nothing else.

Your job is ONLY to extract the engineering architecture from the user's requirement.
Do not design connections yet. Do not invent commercial parts or manufacturers.

RULES:
- Include every functional component needed to satisfy the stated requirement.
- Prefer generic component names unless the user explicitly specifies a part.
- Every component MUST have the interfaces needed for its function.
- Give every interface a unique ID using the component ID as a prefix, for example
  mcu-if-power, mcu-if-sensor, display-if-data.
- Use interface direction: input, output, or bidirectional.
- Use interface type such as power, analog, digital, i2c, spi, uart, can, ethernet,
  wireless, mechanical, control, sensor, display, or another justified type.
- Unknown engineering values are null. Never fabricate manufacturer, part number,
  datasheet, certification, test result, simulation result, or precise limits.
- Requirements must represent the user's actual requirement, not invented requirements.
- Keep the architecture domain-independent.
- Return no systems, connections, resources, or constraints in this stage.
"""


CONNECTION_PROMPT = """
You are OpenBlueprint's interface connection planner.
Return ONE JSON object and nothing else.

Connect the interfaces in the supplied architecture.

RULES:
- You may ONLY use interface IDs appearing in the interface catalog.
- Never invent or modify an interface ID.
- Never use component IDs or system IDs as connection endpoints.
- Connect compatible output/input interfaces where the architecture requires communication,
  power, sensing, control, or other transfer.
- Do not connect unrelated components merely to increase the number of connections.
- If direction is bidirectional, it may connect to another compatible interface.
- Unknown electrical values are null.
- Do not invent manufacturer, part number, test, simulation, certification, or precise limits.
- Return no components, systems, or requirements in this stage.
"""


def _json_prompt(base: str, request: DesignRequest, extra: str) -> str:
    return (
        base
        + f"\nTASK TYPE: {request.task_type}\nDOMAIN: {request.domain or 'general engineering'}"
        + "\nGOALS:\n- " + "\n- ".join(request.goals or ["Create a complete first-pass architecture."])
        + "\nCONSTRAINTS:\n- " + "\n- ".join(request.constraints or ["None provided."])
        + f"\nUSER REQUIREMENT:\n{request.prompt}\n"
        + extra
        + "\nReturn only JSON."
    )


def _parse_json_object(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("AI stage response is not valid JSON.") from exc
    if not isinstance(data, dict):
        raise ValueError("AI stage response must be a JSON object.")
    return data




def _slug(value: str) -> str:
    """Create a deterministic structural ID from model text.

    This is only ID normalization; it does not invent engineering facts.
    """
    import re
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return text or "item"


def _humanize_interface_type(value: str) -> str:
    text = value.replace("_", " ").replace("-", " ").strip()
    return text.title() + " Interface" if text else "Interface"


def _normalize_architecture_payload(data: dict) -> dict:
    """Normalize common small-model structural omissions before strict validation.

    Qwen2.5 3B has been observed to omit IDs/names and to emit requirement
    descriptions as strings even when the requested contract asks for objects.
    We may synthesize deterministic structural identifiers/names, but never
    synthesize engineering values, manufacturers, limits, or other facts.
    """
    normalized = dict(data)

    raw_requirements = normalized.get("requirements", [])
    reqs = []
    for index, item in enumerate(raw_requirements, 1):
        if isinstance(item, str):
            reqs.append({"id": f"req-{index:03d}", "description": item})
        elif isinstance(item, dict):
            item = dict(item)
            item.setdefault("id", f"req-{index:03d}")
            reqs.append(item)
        else:
            raise ValueError("Architecture requirements must be objects or description strings.")
    normalized["requirements"] = reqs

    raw_components = normalized.get("components", [])
    components = []
    used_component_ids: set[str] = set()
    for index, raw in enumerate(raw_components, 1):
        if not isinstance(raw, dict):
            raise ValueError("Architecture components must be objects.")
        component = dict(raw)
        name = str(component.get("name", "")).strip()
        if not name:
            raise ValueError(f"Architecture component {index} is missing a name.")
        base_id = _slug(str(component.get("id") or name))
        component_id = base_id
        suffix = 2
        while component_id in used_component_ids:
            component_id = f"{base_id}-{suffix}"
            suffix += 1
        used_component_ids.add(component_id)
        component["id"] = component_id

        raw_interfaces = component.get("interfaces", [])
        interfaces = []
        used_interface_ids: set[str] = set()
        for int_index, raw_interface in enumerate(raw_interfaces, 1):
            if not isinstance(raw_interface, dict):
                raise ValueError(f"Component {component_id} has a non-object interface.")
            interface = dict(raw_interface)
            interface_type = str(interface.get("type") or "functional").strip()
            base_interface_id = _slug(str(interface.get("id") or f"{component_id}-if-{interface_type}"))
            interface_id = base_interface_id
            suffix = 2
            while interface_id in used_interface_ids:
                interface_id = f"{base_interface_id}-{suffix}"
                suffix += 1
            used_interface_ids.add(interface_id)
            interface["id"] = interface_id
            interface.setdefault("name", _humanize_interface_type(interface_type))
            interface.setdefault("direction", "bidirectional")
            interfaces.append(interface)
        component["interfaces"] = interfaces
        components.append(component)
    normalized["components"] = components
    return normalized


def _build_connection_catalog(stage: ArchitectureStage) -> str:
    rows: list[dict] = []
    for component in stage.components:
        for interface in component.interfaces:
            rows.append({
                "component_id": component.id,
                "component_name": component.name,
                "interface_id": interface.id,
                "name": interface.name,
                "type": interface.type,
                "direction": interface.direction,
                "voltage_min": interface.voltage_min,
                "voltage_max": interface.voltage_max,
                "data_rate": interface.data_rate,
                "unit": interface.unit,
            })
    return "\nINTERFACE CATALOG:\n" + json.dumps(rows, indent=2)


def _normalize_connection_payload(data: dict, stage: ArchitectureStage) -> dict:
    """Normalize observed small-model connection shape without inventing facts.

    Qwen2.5 3B may express an endpoint as a component/interface pair:
    component_id + interface_id and component_id_target + interface_id_target.
    The canonical contract only needs the interface IDs. We therefore translate
    that structural representation, but verify that each interface actually
    belongs to the component named by the model. Missing connection IDs are
    deterministic structural IDs only.
    """
    normalized = dict(data)
    raw_connections = normalized.get("connections", [])
    connections = []
    interface_owner = {
        interface.id: component.id
        for component in stage.components
        for interface in component.interfaces
    }

    for index, raw in enumerate(raw_connections, 1):
        if not isinstance(raw, dict):
            raise ValueError("Connection stage connections must be objects.")
        item = dict(raw)
        item.setdefault("id", f"conn-{index:03d}")

        source = item.get("source")
        target = item.get("target")
        source_component = item.get("component_id")
        source_interface = item.get("interface_id")
        target_component = item.get("component_id_target")
        target_interface = item.get("interface_id_target")

        if source is None and source_interface is not None:
            source = source_interface
        if target is None and target_interface is not None:
            target = target_interface

        if source_component is not None and source_interface is not None:
            owner = interface_owner.get(source_interface)
            if owner != source_component:
                raise ValueError(
                    f"Connection {item['id']} source interface {source_interface!r} "
                    f"does not belong to component {source_component!r}."
                )
        if target_component is not None and target_interface is not None:
            owner = interface_owner.get(target_interface)
            if owner != target_component:
                raise ValueError(
                    f"Connection {item['id']} target interface {target_interface!r} "
                    f"does not belong to component {target_component!r}."
                )

        if source is None or target is None:
            raise ValueError(
                f"Connection {item['id']} must provide source/target interface IDs "
                "or component/interface endpoint pairs."
            )

        item["source"] = source
        item["target"] = target
        # These are only an alternate model-output representation. Do not let
        # them reach the strict StageConnection model.
        for key in ("component_id", "interface_id", "component_id_target", "interface_id_target"):
            item.pop(key, None)
        connections.append(item)

    normalized["connections"] = connections
    for field in ("assumptions", "warnings"):
        values = normalized.get(field, [])
        normalized[field] = [
            value if isinstance(value, str) else json.dumps(value, sort_keys=True)
            for value in values
        ]
    return normalized


def _validate_connection_ids(stage: ArchitectureStage, connection_stage: ConnectionStage) -> None:
    known = {i.id for c in stage.components for i in c.interfaces}
    bad: list[str] = []
    for connection in connection_stage.connections:
        if connection.source not in known:
            bad.append(f"{connection.id}: source={connection.source}")
        if connection.target not in known:
            bad.append(f"{connection.id}: target={connection.target}")
    if bad:
        raise ValueError("Connection stage returned unknown interface IDs: " + "; ".join(bad))


def generate_staged_proposal(request: DesignRequest, provider: AIProvider) -> DesignProposal:
    architecture_raw = provider.generate(
        _json_prompt(ARCHITECTURE_PROMPT, request, "\nReturn: summary, requirements, components, assumptions, warnings.")
    )
    architecture_payload = _normalize_architecture_payload(_parse_json_object(architecture_raw))
    architecture = ArchitectureStage.model_validate(architecture_payload)

    connection_raw = provider.generate(
        _json_prompt(
            CONNECTION_PROMPT,
            request,
            _build_connection_catalog(architecture)
            + "\nReturn: connections, assumptions, warnings.",
        )
    )
    connection_payload = _normalize_connection_payload(_parse_json_object(connection_raw), architecture)
    connection_stage = ConnectionStage.model_validate(connection_payload)
    _validate_connection_ids(architecture, connection_stage)

    components: list[ProposalComponent] = []
    for component in architecture.components:
        components.append(
            ProposalComponent(
                id=component.id,
                name=component.name,
                category=component.category,
                specifications=component.specifications,
                interfaces=[
                    ProposalInterface(
                        id=i.id,
                        name=i.name,
                        type=i.type,
                        direction=i.direction,
                        voltage_min=i.voltage_min,
                        voltage_max=i.voltage_max,
                        current_max=i.current_max,
                        data_rate=i.data_rate,
                        unit=i.unit,
                    )
                    for i in component.interfaces
                ],
            )
        )

    component_ids = [c.id for c in components]
    system = ProposalSystem(
        id="sys-001",
        name="Main System",
        description="First-pass system architecture derived from the user requirement.",
        component_ids=component_ids,
        interfaces=[i.id for c in components for i in c.interfaces],
    )

    requirements = [
        ProposalRequirement(
            id=r.id,
            description=r.description,
            measurable=r.measurable,
            target=r.target,
            min=r.min,
            max=r.max,
            unit=r.unit,
            priority=r.priority,
            verification_method=r.verification_method,
        )
        for r in architecture.requirements
    ]
    connections = [
        ProposalConnection(
            id=c.id,
            name=c.name,
            source=c.source,
            target=c.target,
            interface_type=c.interface_type,
            signal_type=c.signal_type,
            voltage=c.voltage,
            current=c.current,
            data_rate=c.data_rate,
            unit=c.unit,
        )
        for c in connection_stage.connections
    ]

    warnings = [*architecture.warnings, *connection_stage.warnings]
    assumptions = [*architecture.assumptions, *connection_stage.assumptions]
    return DesignProposal(
        summary=architecture.summary,
        status="PROPOSED",
        requirements=requirements,
        systems=[system],
        components=components,
        connections=connections,
        constraints=[],
        resources=[],
        assumptions=assumptions,
        warnings=warnings,
    )
