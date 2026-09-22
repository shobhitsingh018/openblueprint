from pydantic import BaseModel, Field
from typing import Any


class Design(BaseModel):
    id: str
    name: str
    description: str = ""
    version: str = "0.1.0"

    requirements: list[dict[str, Any]] = Field(default_factory=list)
    systems: list[dict[str, Any]] = Field(default_factory=list)
    components: list[dict[str, Any]] = Field(default_factory=list)
    connections: list[dict[str, Any]] = Field(default_factory=list)

    constraints: list[dict[str, Any]] = Field(default_factory=list)
    parameters: list[dict[str, Any]] = Field(default_factory=list)
    resources: list[dict[str, Any]] = Field(default_factory=list)

    validation: dict[str, Any] = Field(default_factory=dict)
    simulation: dict[str, Any] = Field(default_factory=dict)

    bom: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
