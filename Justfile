# Task runner for blabot. See README.md's "Development" section for details.
# Install: https://github.com/casey/just

set shell := ["bash", "-uc"]

# List available recipes
default:
    @just --list

# Install dependencies
sync:
    uv sync

# Run all tests
test:
    uv run pytest -v -s

# Run ProcessIO example tests (fast/simple scenarios)
test-easy:
    cd examples && uv run pytest -v -s -m "simple_process_test and easy" tests/

# Run ProcessIO example tests (complex/slow scenarios)
test-hard:
    cd examples && uv run pytest -v -s -m "simple_process_test and hard" tests/

# Run DeviceIO example tests (needs socat, see examples/README.md)
test-device:
    cd examples && uv run pytest -v -s -m "device_test" tests/

# Run DockerIO example tests (needs the example-app image, see examples/README.md)
test-docker:
    cd examples && uv run pytest -v -s -m "docker_test" tests/

# Run SSHProcessIO example tests (needs REMOTE_* env vars, see examples/README.md)
test-ssh:
    cd examples && uv run pytest -v -s -m "ssh_test" tests/

# Docker-based testing (build + run tests from inside the container)
docker-test:
    cd examples && docker compose build
    cd examples && docker compose run --rm example-app pytest -v -s -m docker_inner_test tests/

# Lint with ruff
lint:
    uv run ruff check .

# Format with ruff
format:
    uv run ruff format .

# Type checking with mypy
typecheck:
    uv run mypy blabot/

# Lint YAML files
yamllint:
    uv run yamllint .

# Lint GitHub Actions workflows (runs in an ephemeral container)
actionlint:
    docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:latest -color

# Run everything the pre-push hook runs (ruff check, mypy, yamllint)
check: lint typecheck yamllint

# One-time setup: installs both pre-commit and pre-push git hooks
precommit-install:
    uv run pre-commit install

# Run pre-commit hooks manually against all files
precommit-run:
    uv run pre-commit run --all-files
    uv run pre-commit run --all-files --hook-stage pre-push
