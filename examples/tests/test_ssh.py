import os
import pytest
import subprocess

from ..cli.example_cli import ExampleCli
from ..cli.blabot.blabot.ssh_io import SSHProcessIO
from ..example import EXAMPLE_FILE_PATH

# This is a remote machine's path
DST_DIR_PATH = "/tmp/"


@pytest.fixture
def ssh_config():
    ssh_config = {}
    ssh_config["user_name"] = os.environ.get("REMOTE_USER_NAME")
    ssh_config["host_name"] = os.environ.get("REMOTE_HOST_NAME")
    ssh_config["key_path"] = os.environ.get("REMOTE_KEY_PATH")

    assert (ssh_config["user_name"] is not None and ssh_config["host_name"] is not None and
            ssh_config["key_path"] is not None), "Set environment variables"

    return ssh_config


@pytest.fixture
def transfer_example(ssh_config):
    # e.g.) scp -i path/to/key/id_fugafuga path/to/example.py hoge@192.168.100.2:/tmp/
    transfer_cmd = [
        "scp", "-i", ssh_config['key_path'], EXAMPLE_FILE_PATH,
        f"{ssh_config['user_name']}@{ssh_config['host_name']}:{DST_DIR_PATH}"
    ]

    subprocess.run(transfer_cmd, check=True)


@pytest.fixture
def ssh_io_cli(ssh_config):
    start_command = "python3 /tmp/example.py"
    prompt = "> "
    io_interact = SSHProcessIO(
        start_command,
        ssh_config["user_name"],
        ssh_config["host_name"],
        ssh_config["key_path"],
        prompt=prompt
    )

    ssh_io_cli = ExampleCli(io_interact)
    ssh_io_cli.start()
    yield ssh_io_cli
    ssh_io_cli.stop()


@pytest.mark.ssh_test
def test_ssh(ssh_config, transfer_example, ssh_io_cli):
    ssh_io_cli.check_startup()
