from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class DesignRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1)
    task_type: Literal["auto", "architecture", "engineering", "coding", "documentation"] = "auto"
    constraints: list[str] = Field(default_factory=list)
    domain: str | None = None
    goals: list[str] = Field(default_factory=list)
    required_outputs: list[str] = Field(default_factory=lambda: [
        "requirements", "systems", "components", "interfaces", "connections", "constraints"
    ])
