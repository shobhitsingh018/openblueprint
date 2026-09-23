from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Constraint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    type: str
    description: str = ""
    parameter: str | None = None
    operator: str | None = None
    value: float | str | bool | None = None
    unit: str | None = None
    severity: str = "ERROR"
    metadata: dict[str, Any] = Field(default_factory=dict)
