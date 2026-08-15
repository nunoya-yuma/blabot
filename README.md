# blabot

## Overview

If development is proceeding in an environment configured as follows

```mermaid
graph LR
    Developer[Developer]

    subgraph Software[Software]
        CLI_Module[CLI Module]
        Module_A[Module A]
    end

    Developer -->|Command| CLI_Module
    CLI_Module -->|Print: result| Developer

    CLI_Module -->|Trigger| Module_A
    Module_A -->|Take action| Module_A
    Module_A -->|Print: result| CLI_Module
```

Our project can automatically control and check inputs and outputs instead of developer.

```mermaid
graph LR
    This_Project[This Project]

    subgraph Software[Software]
        CLI_Module[CLI Module]
        Module_A[Module A]
    end

    This_Project -->|Command| CLI_Module
    CLI_Module -->|Print: result| This_Project

    CLI_Module -->|Trigger| Module_A
    Module_A -->|Take action| Module_A
    Module_A -->|Print: result| CLI_Module
```

## Environment

`uv` environment is recommended.

```shell
cd ${BLABOT}

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and set up development environment
uv sync
```

## Use in other projects

There are several ways to use this package in other projects, but here are two examples.

### Download from GitHub

```shell
pip install git+https://github.com/nunoya-yuma/blabot.git@main
```

### Build from local source code

```shell
cd ${BLABOT}
uv build
pip install dist/blabot-*-py3-none-any.whl
```

## Examples

[Examples](./examples/README.md) are prepared. Please see it if necessary.

An overview description of each class is also available there, so I recommend taking a look at it.

## Architecture

blabot follows a template method pattern: `TemplatedIO` (`blabot/templated_io.py`) defines the
common interface for sending commands and checking outputs, implemented by:

- **ProcessIO** (`blabot/process_io.py`) - local process communication
- **DeviceIO** (`blabot/device_io.py`) - serial device communication
- **SSHProcessIO** (`blabot/ssh_io.py`) - remote process communication via SSH
- **DockerRunIO** / **DockerExecIO** (`blabot/docker_io.py`) - container process communication

See [examples/README.md](./examples/README.md) for a walkthrough of each.

## Development

A [`Justfile`](./Justfile) is provided as a shortcut for the commands below. Install
[`just`](https://github.com/casey/just), then run `just` (or `just --list`) to see all available
recipes (e.g. `just test`, `just lint`, `just check`).

### Testing

This project uses `pytest` with markers to separate test categories.

```shell
# Run all tests
uv run pytest -v -s

# Run specific test categories
uv run pytest -v -s -m "simple_process_test and easy" tests/
uv run pytest -v -s -m "simple_process_test and hard" tests/
uv run pytest -v -s -m "device_test" tests/
uv run pytest -v -s -m "docker_test" tests/
uv run pytest -v -s -m "ssh_test" tests/
```

Device tests need `socat` to simulate a virtual serial device, and SSH tests need
`REMOTE_USER_NAME` / `REMOTE_HOST_NAME` / `REMOTE_KEY_PATH` environment variables pointing at a
reachable host. See [examples/README.md](./examples/README.md) for the full setup steps.

Docker-based testing:

```shell
docker compose build
docker compose run --rm example-app pytest -v -s -m docker_inner_test tests/
```

### Code Quality

```shell
# Lint and format with ruff
uv run ruff check .
uv run ruff format .

# Type checking with mypy
uv run mypy blabot/

# Lint YAML files (config: .yamllint.yaml)
uv run yamllint .

# Lint GitHub Actions workflows (no local install; runs in an ephemeral container)
docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:latest -color
```

### Pre-commit Hooks (optional, local only)

```shell
# One-time setup: installs both pre-commit and pre-push git hooks
uv run pre-commit install

# Run manually against all files
uv run pre-commit run --all-files              # pre-commit stage (ruff format)
uv run pre-commit run --all-files --hook-stage pre-push  # pre-push stage (ruff check, mypy, yamllint)
```

`ruff format` runs on every commit; `ruff check`, `mypy`, and `yamllint` run on push, so frequent
small commits stay fast. This is a local convenience layer only — CI (`ci-tests.yaml`) is still the
source of truth and runs independently of whether hooks are installed. `actionlint` is intentionally
not part of pre-commit; it stays as a CI-only step (`reviewdog/action-actionlint`) for inline PR
annotations.

## CI

GitHub Actions runs the `lint_typecheck_and_test` job on every PR. It lints GitHub Actions workflows
with `actionlint`, lints YAML with `yamllint`, checks formatting and lints with `ruff`, type-checks
with `mypy`, and then runs the unit, example, SSH, Docker, and serial device test suites.

If you want to run GitHub Actions in your local environment, you can use [act command](https://github.com/nektos/act)

```shell
# e.g.)
act -j lint_typecheck_and_test
```

## Release

Releases are triggered by pushing a `vX.Y.Z` tag; `.github/workflows/release.yaml` validates that the
tag matches `pyproject.toml`'s `version`, runs the full CI test suite, builds and pushes the example
app's Docker image to GHCR, and creates a GitHub Release with auto-generated notes.

1. Pick the next version following [SemVer](https://semver.org/) / the
   [Conventional Commits](https://www.conventionalcommits.org/) types used in commit messages since
   the last tag (`git log vX.Y.Z..HEAD --oneline`):
   - Only `fix:` (and non-user-facing `chore:`/`docs:`/`ci:`/`refactor:`/`test:`) → bump **patch**
   - Any `feat:` present → bump **minor**
   - Any breaking change (`!` suffix or `BREAKING CHANGE:` footer) → bump **major**
   - This project is still pre-1.0 (see [SemVer's spec on 0.y.z](https://semver.org/#spec-item-4)), so
     there's no need to rush to `1.0.0`; do that once the public API is expected to stay stable.
2. On a new branch, bump `version` in `pyproject.toml` and run `uv sync` to update `uv.lock`, then open
   a PR and merge it.
3. On `main`, tag the merge commit and push the tag:

   ```shell
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
