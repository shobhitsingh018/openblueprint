import httpx


def check_ollama(base_url: str = "http://127.0.0.1:11434") -> dict:
    try:
        r = httpx.get(base_url.rstrip("/") + "/api/tags", timeout=5)
        r.raise_for_status()
        models = [m.get("name") for m in r.json().get("models", [])]
        return {"available": True, "models": models}
    except Exception as exc:
        return {"available": False, "models": [], "error": str(exc)}


def check_model_available(model: str, base_url: str = "http://127.0.0.1:11434") -> dict:
    """Check both that Ollama is reachable AND that `model` is pulled.

    Returns a dict with `ready` (bool) and a human-readable `message`
    explaining exactly what's wrong when it isn't ready.
    """
    status = check_ollama(base_url)
    if not status["available"]:
        return {
            "ready": False,
            "message": (
                f"Ollama is not reachable at {base_url}.\n"
                f"  - Underlying error: {status['error']}\n"
                "  - Check that Ollama is actually running: 'ollama list' in PowerShell.\n"
                "  - Check it's listening where expected: 'curl http://127.0.0.1:11434/api/tags'.\n"
                "  - If you've set a custom OLLAMA_HOST, set OPENBLUEPRINT_OLLAMA_URL to match it."
            ),
        }
    models = status["models"]
    # Ollama tags can include a variant suffix (e.g. "qwen3:8b-instruct-q4_K_M"),
    # so match on the base name rather than requiring an exact string match.
    if not any(m == model or (m or "").startswith(model.split(":")[0]) for m in models):
        return {
            "ready": False,
            "message": (
                f"Ollama is running at {base_url}, but model '{model}' is not pulled.\n"
                f"  - Installed models: {models or '(none)'}\n"
                f"  - Pull it with: ollama pull {model}"
            ),
        }
    return {"ready": True, "message": f"Ollama is running and '{model}' is available."}
