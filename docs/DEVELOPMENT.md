# Development

## Test

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

## Generate canonical schema

```powershell
python scripts/generate_schema.py
```

## Start API

```powershell
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/`.

## Real local AI

```powershell
ollama list
python -m app.ai.full_pipeline_test
```

The current default local model is `qwen3:8b`. Set `OPENBLUEPRINT_MODEL` to test another installed Ollama model.
