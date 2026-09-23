import os
from pydantic import BaseModel, Field


class AIConfig(BaseModel):
    provider: str = "mock"
    base_url: str = Field(default_factory=lambda: os.getenv("OPENBLUEPRINT_OLLAMA_URL", "http://127.0.0.1:11434"))
    model: str | None = None
    temperature: float = 0.15
    max_tokens: int = 2500
    refinement_passes: int = 1
    timeout: float = Field(default_factory=lambda: float(os.getenv("OPENBLUEPRINT_OLLAMA_TIMEOUT", "180")))
