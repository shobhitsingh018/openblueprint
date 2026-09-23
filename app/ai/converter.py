from app.ai.proposal import DesignProposal, ProposalComponent, ProposalConnection, ProposalConstraint, ProposalInterface, ProposalRequirement, ProposalResource, ProposalSystem
from app.core.component import Component
from app.core.connection import Connection
from app.core.constraint import Constraint
from app.core.design import Design
from app.core.interface import Interface
from app.core.requirement import Requirement
from app.core.resource import Resource
from app.core.system import System


def _convert_requirement(d: ProposalRequirement) -> Requirement:
    return Requirement(id=d.id, type=d.type, description=d.description, measurable=d.measurable,
                       target_value=d.target, minimum_value=d.min, maximum_value=d.max,
                       unit=d.unit, priority=d.priority, verification_method=d.verification_method,
                       metadata=d.metadata)


def _convert_interface(d: ProposalInterface, component_id: str, index: int) -> Interface:
    return Interface(id=d.id or f"{component_id}-if-{index:03d}", name=d.name, type=d.type,
                     direction=d.direction, voltage_min=d.voltage_min, voltage_max=d.voltage_max,
                     current_max=d.current_max, data_rate=d.data_rate, unit=d.unit,
                     metadata={**d.metadata, "source_component": component_id})


def _convert_component(d: ProposalComponent) -> Component:
    return Component(id=d.id, name=d.name, category=d.category, manufacturer=d.manufacturer,
                     part_number=d.part_number, specifications=d.specifications,
                     interfaces=[_convert_interface(i, d.id, n) for n, i in enumerate(d.interfaces, 1)],
                     voltage_min=d.voltage_min, voltage_max=d.voltage_max, current_max=d.current_max,
                     power_max=d.power_max, weight=d.weight, cost=d.cost, datasheet=d.datasheet,
                     simulation_model=d.simulation_model, metadata=d.metadata)


def _convert_system(d: ProposalSystem) -> System:
    return System(id=d.id, name=d.name, description=d.description, parent_id=d.parent_id,
                  subsystem_ids=d.subsystem_ids, component_ids=d.component_ids, interfaces=d.interfaces,
                  parameters=d.parameters, constraints=d.constraints, metadata=d.metadata)


def _convert_connection(d: ProposalConnection) -> Connection:
    return Connection(id=d.id, name=d.name, source=d.source, target=d.target,
                      interface_type=d.interface_type, signal_type=d.signal_type, voltage=d.voltage,
                      current=d.current, data_rate=d.data_rate, unit=d.unit, parameters=d.parameters,
                      metadata=d.metadata)


def _convert_constraint(d: ProposalConstraint) -> Constraint:
    return Constraint(id=d.id, name=d.name, type=d.type, description=d.description,
                      parameter=d.parameter, operator=d.operator, value=d.value, unit=d.unit,
                      severity=d.severity, metadata=d.metadata)


def _convert_resource(d: ProposalResource) -> Resource:
    return Resource(id=d.id, name=d.name, type=d.type, capacity=d.capacity, allocated=d.allocated,
                    unit=d.unit, source=d.source, metadata=d.metadata)


def proposal_to_design(proposal: DesignProposal, design_id: str, name: str) -> Design:
    return Design(
        id=design_id, name=name, description=proposal.summary,
        requirements=[_convert_requirement(x) for x in proposal.requirements],
        systems=[_convert_system(x) for x in proposal.systems],
        components=[_convert_component(x) for x in proposal.components],
        connections=[_convert_connection(x) for x in proposal.connections],
        constraints=[_convert_constraint(x) for x in proposal.constraints],
        resources=[_convert_resource(x) for x in proposal.resources],
        metadata={"ai": {"status": proposal.status, "assumptions": proposal.assumptions,
                           "warnings": proposal.warnings}},
    )
