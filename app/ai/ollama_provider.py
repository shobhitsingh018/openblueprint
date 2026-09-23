from typing import Any

import httpx

from app.ai.provider import AIProvider


class OllamaProvider(AIProvider):
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5:3b-instruct",
        temperature: float = 0.15,
        max_tokens: int = 2500,
        timeout: float = 180.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def generate(self, prompt: str, response_schema: dict[str, Any] | None = None) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        # Ollama supports either the generic JSON mode or a JSON Schema object.
        # OpenBlueprint uses the exact Pydantic proposal schema to prevent
        # field-name drift such as `current_draw` vs `current`.
        payload["format"] = response_schema if response_schema else "json"

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
        except httpx.ConnectError as exc:
            raise RuntimeError(
                f"Could not reach Ollama at {self.base_url}. "
                "The server refused the connection, which usually means one of:\n"
                "  1) Ollama is not actually running right now (check the system tray icon, "
                "or run 'ollama list' in a terminal - if that hangs/fails, Ollama is down).\n"
                "  2) Ollama is bound to a different host/port because OLLAMA_HOST is set to "
                "something other than 127.0.0.1:11434 on this machine. Run "
                "'echo $env:OLLAMA_HOST' in PowerShell to check, and if it's set, either unset "
                "it or pass that URL via the OPENBLUEPRINT_OLLAMA_URL environment variable.\n"
                "  3) A firewall/VPN/antivirus is blocking local loopback connections from "
                "Python. Try 'curl http://127.0.0.1:11434/api/tags' in PowerShell - if that "
                "also fails, it's not this code, it's the local network/security stack.\n"
                f"Underlying error: {exc}"
            ) from exc
        except httpx.TimeoutException as exc:
            raise RuntimeError(
                f"Ollama at {self.base_url} accepted the connection but did not respond within "
                f"{self.timeout}s. The model '{self.model}' may still be loading into memory on "
                "first use, or your machine may not have enough RAM/VRAM for it - try running "
                "'ollama run " + self.model + "' directly in a terminal first to warm it up and "
                "confirm it works at all."
            ) from exc

        if getattr(response, "status_code", None) == 404:
            raise RuntimeError(
                f"Ollama responded but model '{self.model}' was not found at {self.base_url}. "
                f"Pull it first with: ollama pull {self.model}\n"
                "Run 'ollama list' to see exactly what tag is installed - the name must match "
                "exactly, including the ':8b' suffix."
            )
        response.raise_for_status()
        result = response.json()
        text = result.get("response")
        if not isinstance(text, str):
            raise ValueError("Ollama returned no text response.")
        return text
