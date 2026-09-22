from pydantic import BaseModel


class ModelProfile(BaseModel):
    name: str
    provider: str = "ollama"

    roles: list[str]

    context_length: int = 8192

    description: str = ""


MODEL_PROFILES = {
    "general": ModelProfile(
        name="qwen3:8b",
        roles=["architecture", "documentation"],
        context_length=32768,
        description="General reasoning and system architecture.",
    ),

    "coding": ModelProfile(
        name="qwen3-coder:latest",
        roles=["coding"],
        context_length=32768,
        description="Software, firmware and code generation.",
    ),

    "engineering": ModelProfile(
        name="qwen3:8b",
        roles=["engineering"],
        context_length=32768,
        description="Engineering reasoning and component analysis.",
    ),
}
