from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Interface(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
