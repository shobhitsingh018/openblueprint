from typing import Any, Literal
from pydantic import BaseModel, Field


class DesignProposal(BaseModel):
    summary: str

    status: Literal[
        "PROPOSED",
        "APPROVED",
        "REJECTED",
        "APPLIED",
    ] = "PROPOSED"

    requirements: list[dict[str, Any]] = Field(default_factory=list)
    systems: list[dict[str, Any]] = Field(default_factory=list)
    components: list[dict[str, Any]] = Field(default_factory=list)
    connections: list[dict[str, Any]] = Field(default_factory=list)

    constraints: list[dict[str, Any]] = Field(default_factory=list)
    resources: list[dict[str, Any]] = Field(default_factory=list)

    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
