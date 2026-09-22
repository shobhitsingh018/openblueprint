from app.ai.config import AIConfig
from app.ai.mock_provider import MockProvider
from app.ai.ollama_provider import OllamaProvider
from app.ai.provider import AIProvider


def create_provider(config: AIConfig) -> AIProvider:

    if config.provider == "mock":
        return MockProvider()

    if config.provider == "ollama":
        if not config.model:
            raise ValueError("Ollama requires a model name.")

        return OllamaProvider(
            base_url=config.base_url or "http://127.0.0.1:11434",
            model=config.model,
        )

    raise ValueError(
        f"Unsupported AI provider: {config.provider}"
    )
