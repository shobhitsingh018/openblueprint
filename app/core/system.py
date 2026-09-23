from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class System(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
