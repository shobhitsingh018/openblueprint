# OpenBlueprint

OpenBlueprint is an open-source, local-first AI engineering and design platform.
The canonical Design Model is the source of truth. AI produces proposals; deterministic validation decides whether a design is structurally ready.

## Current MVP
- Python 3.11–3.13
- FastAPI API
- Pydantic canonical design model
- Strict AI proposal schema
- Ollama provider
- Qwen3 8B as the current local model
- Deterministic validation and readiness states: VALID, INCOMPLETE, INVALID
- AI refinement pass for incomplete first-pass architectures
- Generated canonical JSON Schema
- Minimal browser UI placeholder kept out of the critical backend path

## Run

```powershell
cd D:\OpenBlueprint
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Health: `http://127.0.0.1:8000/api/v1/health`

AI health: `http://127.0.0.1:8000/api/v1/ai/health`

## Real Qwen3 test

Ensure Ollama is running and `qwen3:8b` is installed:

```powershell
ollama list
python -m app.ai.full_pipeline_test
```

The test executes:

`Requirement → Qwen3 → strict proposal parsing → canonical Design → deterministic validation → readiness`

## Architecture

```text
User Requirement
      ↓
DesignRequest
      ↓
Task Router / Model Profile
      ↓
Ollama / Local Model
      ↓
Strict DesignProposal
      ↓
Proposal → Canonical Design converter
      ↓
Deterministic validation
      ↓
VALID / INCOMPLETE / INVALID
```

AI does not directly mutate the canonical design. Commercial component data, simulation results, certification, and test evidence must come from explicit future registries/adapters rather than model invention.

## API

- `GET /api/v1/health`
- `GET /api/v1/ai/health`
- `POST /api/v1/design/propose`
- `POST /api/v1/design/validate`
- `POST /api/v1/design/proposal-to-design`

## License
MIT


## v2.4 AI pipeline
Ollama generation now uses a staged architecture flow: architecture decomposition first, interface-aware connection planning second, then deterministic canonical assembly and validation. The pipeline defaults to `qwen2.5:3b-instruct`; override with `OPENBLUEPRINT_MODEL`. Malformed connection endpoints are rejected rather than silently rewired.
