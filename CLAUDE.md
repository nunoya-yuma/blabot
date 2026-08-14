# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Full project documentation — setup, the complete test/lint/build command reference, pre-commit
hooks, CI details, and architecture — lives in [README.md](./README.md) and
[examples/README.md](./examples/README.md). This file only adds what's specific to working here
as Claude Code; keep it short and let the READMEs stay the single source of truth for commands.

## Quick Commands

```bash
uv sync                             # install dependencies
uv run pytest -v -s                 # run all tests
uv run ruff check . && uv run ruff format .
uv run mypy blabot/
```

A `Justfile` wraps these and more (`just test`, `just lint`, `just check`, ...) — run `just --list`
for the full recipe list.

For the full test marker list (device/SSH/Docker tests and their env var requirements), code
quality tooling, pre-commit hook setup, and CI job details, see README.md's "Development" section.

## Architecture

blabot is a Python library for automated CLI testing and process interaction, built around a
template method pattern: `TemplatedIO` (`blabot/templated_io.py`) is the abstract base, implemented
by `ProcessIO`, `DeviceIO`, `SSHProcessIO`, and `DockerRunIO`/`DockerExecIO`. See README.md's
"Architecture" section for the one-line summary of each, or examples/README.md for a full
walkthrough.

## Key Files

- `examples/example_app.py` - Sample CLI application used for testing
- `examples/tests/` - Comprehensive test suite with various scenarios
- `examples/docker-compose.yaml` - Container orchestration for testing

## Development Guidelines

- Always run `uv run ruff check .` and `pytest` after code changes
- Use English for code comments and variable names
- Create feature branches from main, then submit PRs for integration
