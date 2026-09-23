# OpenBlueprint Architecture

```text
                    ┌──────────────────────┐
                    │   User Requirement   │
                    └──────────┬───────────┘
                               │
                         DesignRequest
                               │
                    ┌──────────▼───────────┐
                    │ Task Router / Model  │
                    │      Orchestrator    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Local AI Provider    │
                    │      Ollama          │
                    └──────────┬───────────┘
                               │
                       DesignProposal
                               │
                    ┌──────────▼───────────┐
                    │ Proposal Converter   │
                    │ AI → Canonical Model │
                    └──────────┬───────────┘
                               │
                         Canonical Design
                               │
                    ┌──────────▼───────────┐
                    │ Deterministic Rules  │
                    └──────────┬───────────┘
                               │
                    VALID / INCOMPLETE / INVALID
```

The proposal and canonical model are deliberately separate. This prevents an LLM response from becoming engineering truth merely because it parsed as JSON.

## Extension points
- `app/components/`: future component registry and verified part data.
- `app/simulation/`: simulation adapters.
- `app/projects/`: future project persistence and versioning.
- `app/validation/`: future domain-specific validation packages.
- `app/ai/models.py`: model profiles and future specialist routing.
