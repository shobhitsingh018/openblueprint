from pydantic import BaseModel


class AIConfig(BaseModel):
    provider: str = "mock"

    base_url: str | None = None
    model: str | None = None

    temperature: float = 0.2
    max_tokens: int = 4096
