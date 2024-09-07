from nn_io_interact.nn_io_interact.ssh_io import SSHProcessIO
import os
import pytest
import subprocess

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_FILE_PATH = os.path.join(PARENT_DIR, "example.py")

# This is a remote machine's path
DST_DIR_PATH = "/tmp/"


@pytest.fixture
def ssh_config():
    ssh_config = {}
    ssh_config["user_name"] = os.environ.get("REMOTE_USER_NAME")
    ssh_config["host_name"] = os.environ.get("REMOTE_HOST_NAME")
    ssh_config["key_path"] = os.environ.get("REMOTE_KEY_PATH")

    assert ssh_config["user_name"] is not None and ssh_config["host_name"] is not None and \
        ssh_config["key_path"] is not None, "Set environment variables"

    return ssh_config


@pytest.fixture
def transfer_example(ssh_config):
    assert os.path.exists(SRC_FILE_PATH), "Example file does not exist"

    # e.g.) scp -i path/to/key/id_rsa_hoge path/to/example.py hoge@hostname:/tmp/
    transfer_cmd = [
        "scp", "-i", ssh_config['key_path'], SRC_FILE_PATH,
        f"{ssh_config['user_name']}@{ssh_config['host_name']}:{DST_DIR_PATH}"
    ]

    subprocess.run(transfer_cmd, check=True)


@pytest.fixture
def ssh_io_cli(ssh_config):
    start_command = "python3 /tmp/example.py"
    ssh_io_cli = SSHProcessIO(ssh_config["user_name"], ssh_config["host_name"],
                              ssh_config["key_path"], start_command)
    ssh_io_cli.start()
    yield ssh_io_cli
    ssh_io_cli.stop()


def test_ssh(ssh_config, transfer_example, ssh_io_cli):
    assert ssh_io_cli.wait_for("Initializing...")
    assert ssh_io_cli.wait_for("Complete startup sequence")
