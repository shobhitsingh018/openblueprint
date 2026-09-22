from typing import Literal

from pydantic import BaseModel, Field


class DesignRequest(BaseModel):
    prompt: str

    task_type: Literal[
        "auto",
        "architecture",
        "engineering",
        "coding",
        "documentation",
    ] = "auto"

    constraints: list[str] = Field(default_factory=list)

    domain: str | None = None

    goals: list[str] = Field(default_factory=list)

    required_outputs: list[str] = Field(
        default_factory=lambda: [
            "requirements",
            "systems",
            "components",
            "connections",
            "constraints",
        ]
    )
