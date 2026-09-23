import os
from app.ai.health import check_model_available, check_ollama

if __name__ == "__main__":
    base_url = os.getenv("OPENBLUEPRINT_OLLAMA_URL", "http://127.0.0.1:11434")
    model = os.getenv("OPENBLUEPRINT_MODEL", "qwen3:8b")

    print(f"Checking Ollama at {base_url} ...")
    result = check_ollama(base_url)
    print(result)

    print(f"\nChecking model '{model}' is pulled ...")
    check = check_model_available(model, base_url)
    print(check["message"])
    print("\nReady for full_pipeline_test.py:" , check["ready"])
