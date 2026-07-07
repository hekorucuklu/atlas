# Atlas

Atlas is a long-term Python project in its initial bootstrap phase.

## Status

This repository currently contains only the minimal scaffolding needed to start an MVP safely. Business logic has not been implemented yet.

## Requirements

- Python 3.12+
- uv

## Setup

Install dependencies:

```bash
uv sync --dev
```

Run the CLI:

```bash
uv run atlas --help
```

Run tests:

```bash
uv run pytest
```

Run pre-commit checks:

```bash
uv run pre-commit run --all-files
```

## Project Shape

- `apps/cli/main.py` contains the Typer CLI entry point.
- `tests/` contains the pytest suite.
- `AGENTS.md` captures collaboration and implementation guidance for future agent work.
