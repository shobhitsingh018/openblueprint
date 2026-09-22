import httpx


def check_ollama(base_url: str = "http://127.0.0.1:11434") -> bool:
    try:
        response = httpx.get(
            f"{base_url.rstrip('/')}/api/tags",
            timeout=5.0,
        )
        return response.is_success
    except httpx.HTTPError:
        return False


if __name__ == "__main__":
    print("Ollama available:", check_ollama())
