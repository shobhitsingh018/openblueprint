from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Requirement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    type: str
    description: str
    measurable: bool = False
    target_value: float | None = None
    minimum_value: float | None = None
    maximum_value: float | None = None
    unit: str | None = None
    priority: str = "normal"
    verification_method: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
