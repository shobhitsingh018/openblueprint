from typing import Any
from pydantic import BaseModel, Field


class Constraint(BaseModel):
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
