from typing import Any
from pydantic import BaseModel, Field


class Resource(BaseModel):
    id: str
    name: str
    type: str

    capacity: float | None = None
    allocated: float = 0.0

    unit: str | None = None

    source: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
