from app.ai.config import AIConfig
from app.ai.factory import create_provider


def check_provider(config: AIConfig) -> dict:
    try:
        provider = create_provider(config)

        return {
            "provider": config.provider,
            "available": True,
            "provider_type": type(provider).__name__,
        }

    except Exception as exc:
        return {
            "provider": config.provider,
            "available": False,
            "error": str(exc),
        }
