from typing import Any
from pydantic import BaseModel, Field


class Connection(BaseModel):
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
