from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from app.core.interface import Interface


class Component(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    category: str = "unknown"
    manufacturer: str | None = None
    part_number: str | None = None
    specifications: dict[str, Any] = Field(default_factory=dict)
    interfaces: list[Interface] = Field(default_factory=list)
    voltage_min: float | None = None
    voltage_max: float | None = None
    current_max: float | None = None
    power_max: float | None = None
    weight: float | None = None
    cost: float | None = None
    datasheet: str | None = None
    simulation_model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
