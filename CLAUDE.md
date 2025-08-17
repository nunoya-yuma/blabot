# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

This project uses uv for dependency management:

```bash
uv sync
```

## Common Commands

### Testing
```bash
# Run all tests
uv run pytest -v -s

# Run specific test categories
uv run pytest -v -s -m "simple_process_test and easy" tests/
uv run pytest -v -s -m "simple_process_test and hard" tests/
uv run pytest -v -s -m "device_test" tests/
uv run pytest -v -s -m "docker_test" tests/
uv run pytest -v -s -m "ssh_test" tests/

# Docker-based testing
docker compose build
docker compose run --rm example-app pytest -v -s -m docker_inner_test tests/
```

### Building and Installation
```bash
uv build
pip install dist/blabot-0.1.0-py3-none-any.whl
```

### Code Quality
```bash
# Lint and format with ruff
uv run ruff check .
uv run ruff format .

# Type checking with mypy
uv run mypy blabot/
```

### Local CI Testing
```bash
act -j ruff_and_pytest
```

## Architecture

**blabot** is a Python library for automated CLI testing and process interaction. It provides a unified interface through a template method pattern:

- **TemplatedIO** (base class in `blabot/templated_io.py`) - Abstract interface for all I/O operations
- **ProcessIO** (`blabot/process_io.py`) - Local process communication
- **DeviceIO** (`blabot/device_io.py`) - Serial device communication
- **SSHProcessIO** (`blabot/ssh_io.py`) - Remote SSH process communication
- **DockerRunIO/DockerExecIO** (`blabot/docker_io.py`) - Container process communication

## Test Environment Setup

### SSH Testing
Requires environment variables:
```bash
export REMOTE_USER_NAME="username"
export REMOTE_HOST_NAME="192.168.100.2"
export REMOTE_KEY_PATH="${HOME}/.ssh/id_key"
```

### Device Testing
Requires `socat` for virtual device simulation:
```bash
sudo apt install socat
```

## Key Files

- `examples/example_app.py` - Sample CLI application used for testing
- `examples/tests/` - Comprehensive test suite with various scenarios
- `examples/docker-compose.yaml` - Container orchestration for testing

## Development Guidelines

- Always run `uv run ruff check .` and `pytest` after code changes
- Use English for code comments and variable names
- Create feature branches from main, then submit PRs for integration
