import pytest
import subprocess

from cli.example_cli import ExampleCli
from cli.nn_io_interact.nn_io_interact.docker_io import DockerProcessIO
from cli.nn_io_interact.nn_io_interact.process_io import ProcessIO

START_COMMAND = "python3 /app/example.py"
DOCKER_IMAGE_NAME = "nn/example-app:latest"
DOCKER_CONTAINER_NAME = "example_app"


@pytest.fixture
def docker_io_cli():
    PROMPT = "> "
    io_interact = DockerProcessIO(
        START_COMMAND,
        DOCKER_IMAGE_NAME,
        DOCKER_CONTAINER_NAME,
        prompt=PROMPT,
    )

    docker_io_cli = ExampleCli(io_interact)
    docker_io_cli.start()
    yield docker_io_cli
    docker_io_cli.stop()


@pytest.fixture
def docker_io_exec_cli():
    docker_run_command = [
        "docker",
        "run",
        "-dit",
        "--name",
        DOCKER_CONTAINER_NAME,
        DOCKER_IMAGE_NAME,
        "bash"]
    res_run = subprocess.run(docker_run_command)
    assert res_run.returncode == 0, "Failed to run docker container"

    docker_exec_command = ["docker", "exec", "-i", DOCKER_CONTAINER_NAME, "ls", "-a"]
    res_ls = subprocess.run(docker_exec_command)
    assert res_ls.returncode == 0, "Failed to run docker sample command"

    PROMPT = "> "
    io_interact = DockerProcessIO(
        START_COMMAND,
        DOCKER_IMAGE_NAME,
        DOCKER_CONTAINER_NAME,
        True,
        prompt=PROMPT
    )

    docker_io_exec_cli = ExampleCli(io_interact)
    docker_io_exec_cli.start()
    yield docker_io_exec_cli
    docker_io_exec_cli.stop()


@pytest.fixture
def docker_io_inner_cli():
    PROMPT = "> "
    io_interact = ProcessIO(START_COMMAND, PROMPT)

    docker_io_inner_cli = ExampleCli(io_interact)
    docker_io_inner_cli.start()
    yield docker_io_inner_cli
    docker_io_inner_cli.stop()


@pytest.mark.docker_test
def test_docker_simple(docker_io_cli):
    docker_io_cli.check_startup()


@pytest.mark.docker_test
def test_docker_exec(docker_io_exec_cli):
    docker_io_exec_cli.check_startup()


@pytest.mark.docker_inner_test
def test_docker_inner(docker_io_inner_cli):
    docker_io_inner_cli.check_startup()
