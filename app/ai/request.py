from pydantic import BaseModel, Field


class DesignRequest(BaseModel):
    prompt: str

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
