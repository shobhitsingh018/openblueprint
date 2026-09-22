import httpx

from app.ai.provider import AIProvider


class OllamaProvider(AIProvider):

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "openblueprint",
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]
