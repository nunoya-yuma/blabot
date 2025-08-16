import os
import subprocess

import pytest

from blabot.ssh_io import SSHConfig, SSHProcessIO
from examples.example_app import EXAMPLE_FILE_PATH, EXAMPLE_PROMPT
from examples.example_cli import ExampleCli

# This is a remote machine's path
DST_DIR_PATH = "/tmp/"


@pytest.fixture
def ssh_config():
    ssh_config = {}
    ssh_config["user_name"] = os.environ.get("REMOTE_USER_NAME")
    ssh_config["host_name"] = os.environ.get("REMOTE_HOST_NAME")
    ssh_config["key_path"] = os.environ.get("REMOTE_KEY_PATH")

    assert ssh_config["user_name"] is not None, (
        "Set environment variable REMOTE_USER_NAME"
    )
    assert ssh_config["host_name"] is not None, (
        "Set environment variable REMOTE_HOST_NAME"
    )
    assert ssh_config["key_path"] is not None, (
        "Set environment variable REMOTE_KEY_PATH"
    )

    return ssh_config


@pytest.fixture
def transfer_example(ssh_config):
    # e.g.)
    # scp -i path/to/key/id_fugafuga path/to/example_app.py hoge@192.168.100.2:/tmp/ # noqa: E501
    transfer_cmd = [
        "scp",
        "-i",
        ssh_config["key_path"],
        EXAMPLE_FILE_PATH,
        f"{ssh_config['user_name']}@{ssh_config['host_name']}:{DST_DIR_PATH}",
    ]

    subprocess.run(transfer_cmd, check=True)


@pytest.fixture
def ssh_io_cli(ssh_config):
    start_command = "python3 /tmp/example_app.py"
    ssh_config_obj = SSHConfig(
        user_name=ssh_config["user_name"],
        host_name=ssh_config["host_name"],
        key_path=ssh_config["key_path"],
    )
    io_interact = SSHProcessIO(
        start_command,
        ssh_config_obj,
        prompt=EXAMPLE_PROMPT,
    )

    ssh_io_cli = ExampleCli(io_interact)
    ssh_io_cli.start()
    yield ssh_io_cli
    ssh_io_cli.stop()


@pytest.mark.ssh_test
@pytest.mark.usefixtures("ssh_config", "transfer_example")
def test_ssh(ssh_io_cli):
    ssh_io_cli.check_startup()
