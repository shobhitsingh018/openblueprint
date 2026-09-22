from pydantic import BaseModel, Field


class DesignRequest(BaseModel):
    prompt: str
    constraints: list[str] = Field(default_factory=list)
    domain: str | None = None
