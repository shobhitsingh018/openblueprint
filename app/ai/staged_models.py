from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class StrictStageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StageRequirement(StrictStageModel):
    id: str
    description: str
    measurable: bool = False
    target: float | None = None
    min: float | None = None
    max: float | None = None
    unit: str | None = None
    priority: str = "normal"
    verification_method: str | None = None


class StageInterface(StrictStageModel):
    id: str
    name: str
    type: str
    direction: str = "bidirectional"
    voltage_min: float | None = None
    voltage_max: float | None = None
    current_max: float | None = None
    data_rate: float | None = None
    unit: str | None = None


class StageComponent(StrictStageModel):
    id: str
    name: str
    category: str = "unknown"
    interfaces: list[StageInterface] = Field(default_factory=list)
    specifications: dict[str, Any] = Field(default_factory=dict)


class ArchitectureStage(StrictStageModel):
    summary: str
    requirements: list[StageRequirement] = Field(default_factory=list)
    components: list[StageComponent] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class StageConnection(StrictStageModel):
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


class ConnectionStage(StrictStageModel):
    connections: list[StageConnection] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
