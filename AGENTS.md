# Agent Guidance

Atlas is in the MVP bootstrap phase. Keep changes small, typed, and easy to review.

## Ground Rules

- Use Python 3.12+.
- Use uv for dependency management and command execution.
- Use Typer for CLI surfaces.
- Use pytest for tests.
- Do not add business logic until the project scope is defined.
- Do not add FastAPI, Docker, Kubernetes, Kafka, Redis, Qdrant, or other infrastructure dependencies without an explicit project decision.
- Keep modules under roughly 300 lines where practical.
- Prefer clear typed functions over early abstractions.

## Useful Commands

```bash
uv sync --dev
uv run atlas --help
uv run pytest
uv run pre-commit run --all-files
```

## Review Expectations

Every change should explain its purpose, stay within the requested scope, and include focused tests when behavior changes.
