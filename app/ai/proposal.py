from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProposalRequirement(StrictModel):
    id: str
    type: str = "user_defined"
    description: str
    measurable: bool = False
    target: float | None = None
    min: float | None = None
    max: float | None = None
    unit: str | None = None
    priority: str = "normal"
    verification_method: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalInterface(StrictModel):
    id: str
    name: str
    type: str = "unknown"
    direction: str = "bidirectional"
    voltage_min: float | None = None
    voltage_max: float | None = None
    current_max: float | None = None
    data_rate: float | None = None
    unit: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalSystem(StrictModel):
    id: str
    name: str
    description: str = ""
    parent_id: str | None = None
    subsystem_ids: list[str] = Field(default_factory=list)
    component_ids: list[str] = Field(default_factory=list)
    interfaces: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalComponent(StrictModel):
    id: str
    name: str
    category: str = "unknown"
    manufacturer: str | None = None
    part_number: str | None = None
    specifications: dict[str, Any] = Field(default_factory=dict)
    interfaces: list[ProposalInterface] = Field(default_factory=list)
    voltage_min: float | None = None
    voltage_max: float | None = None
    current_max: float | None = None
    power_max: float | None = None
    weight: float | None = None
    cost: float | None = None
    datasheet: str | None = None
    simulation_model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalConnection(StrictModel):
    id: str
    name: str = ""
    source: str
    target: str
    interface_type: str | None = None
    signal_type: str | None = None
    voltage: float | None = None
    current: float | None = None
    data_rate: float | None = None
    unit: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalConstraint(StrictModel):
    id: str
    name: str
    type: str = "engineering"
    description: str = ""
    parameter: str | None = None
    operator: str | None = None
    value: float | str | bool | None = None
    unit: str | None = None
    severity: str = "ERROR"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProposalResource(StrictModel):
    id: str
    name: str
    type: str
    capacity: float | None = None
    allocated: float = 0.0
    unit: str | None = None
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DesignProposal(StrictModel):
    summary: str
    status: Literal["PROPOSED", "APPROVED", "REJECTED", "APPLIED"] = "PROPOSED"
    requirements: list[ProposalRequirement] = Field(default_factory=list)
    systems: list[ProposalSystem] = Field(default_factory=list)
    components: list[ProposalComponent] = Field(default_factory=list)
    connections: list[ProposalConnection] = Field(default_factory=list)
    constraints: list[ProposalConstraint] = Field(default_factory=list)
    resources: list[ProposalResource] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
