import pytest
import subprocess

from nn_io_interact.nn_io_interact.docker_io import DockerProcessIO
from nn_io_interact.nn_io_interact.process_io import ProcessIO

START_COMMAND = "python3 /app/example.py"
DOCKER_IMAGE_NAME = "nn/example-app:latest"
DOCKER_CONTAINER_NAME = "example_app"


@pytest.fixture
def docker_io_cli():
    PROMPT = "> "
    docker_io_cli = DockerProcessIO(
        START_COMMAND,
        DOCKER_IMAGE_NAME,
        DOCKER_CONTAINER_NAME,
        prompt=PROMPT,
    )
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
    docker_io_exec_cli = DockerProcessIO(
        START_COMMAND,
        DOCKER_IMAGE_NAME,
        DOCKER_CONTAINER_NAME,
        False,
        prompt=PROMPT
    )

    docker_io_exec_cli.start()
    yield docker_io_exec_cli
    docker_io_exec_cli.stop()

    docker_remove_command = [
        "docker", "rm", "-f", DOCKER_CONTAINER_NAME
    ]
    res_remove = subprocess.run(docker_remove_command, stdout=subprocess.DEVNULL)
    assert res_remove.returncode == 0, "Failed to remove docker container"


@pytest.fixture
def docker_io_inner_cli():
    PROMPT = "> "
    docker_io_inner_cli = ProcessIO(START_COMMAND, PROMPT)
    docker_io_inner_cli.start()
    yield docker_io_inner_cli
    docker_io_inner_cli.stop()


@pytest.mark.docker_test
def test_docker_simple(docker_io_cli):
    assert docker_io_cli.wait_for("Initializing...")
    assert docker_io_cli.wait_for("Complete startup sequence")

    assert docker_io_cli.run_command("sample-ctrl on", "Sample status changed to 'on'")


@pytest.mark.docker_test
def test_docker_exec(docker_io_exec_cli):
    assert docker_io_exec_cli.wait_for("Initializing...")
    assert docker_io_exec_cli.wait_for("Complete startup sequence")

    assert docker_io_exec_cli.run_command("sample-ctrl off", "Sample status changed to 'off'")


@pytest.mark.docker_inner_test
def test_docker_inner(docker_io_inner_cli):
    assert docker_io_inner_cli.wait_for("Initializing...")
    assert docker_io_inner_cli.wait_for("Complete startup sequence")

    assert docker_io_inner_cli.run_command("sample-ctrl on", "Sample status changed to 'on'")
