from app.ai.config import AIConfig
from app.ai.mock_provider import MockProvider
from app.ai.provider import AIProvider


def create_provider(config: AIConfig) -> AIProvider:

    if config.provider == "mock":
        return MockProvider()

    raise ValueError(
        f"Unsupported AI provider: {config.provider}"
    )
