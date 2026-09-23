from dataclasses import dataclass


@dataclass(frozen=True)
class ModelProfile:
    name: str
    roles: tuple[str, ...]
    context_length: int
    description: str


MODEL_PROFILES = {
    "general": ModelProfile("qwen2.5:3b-instruct", ("architecture", "documentation"), 32768,
                             "General local reasoning and architecture model."),
    "engineering": ModelProfile("qwen2.5:3b-instruct", ("engineering",), 32768,
                                 "Engineering architecture and interface reasoning."),
    "coding": ModelProfile("qwen2.5:3b-instruct", ("coding",), 32768,
                            "Initial local coding model; replace with a coding specialist later."),
}
