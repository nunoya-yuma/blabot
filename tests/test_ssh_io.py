"""Unit tests for SSHProcessIO class."""

from unittest.mock import MagicMock, patch

import pexpect
import pytest

from blabot.ssh_io import SSHConfig, SSHProcessIO

# =============================================================================
# start() tests
# =============================================================================


@pytest.mark.unit
def test_start_spawns_ssh_and_sends_command():
    """start() should spawn SSH login, wait for prompt, then send start_command."""
    config = SSHConfig(
        user_name="testuser",
        host_name="192.168.1.100",
        key_path="/home/user/.ssh/id_rsa",
    )
    io = SSHProcessIO(
        start_command="python app.py",
        ssh_config=config,
        newline="\n",
    )

    with patch("blabot.ssh_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.after = b"$"
        mock_spawn.return_value = mock_process

        io.start()

        mock_spawn.assert_called_once_with(
            "ssh -i /home/user/.ssh/id_rsa testuser@192.168.1.100"
        )
        mock_process.sendline.assert_called_with("python app.py\n")


@pytest.mark.unit
def test_start_raises_when_login_fails():
    """start() should raise RuntimeError when SSH login times out."""
    config = SSHConfig(
        user_name="testuser",
        host_name="192.168.1.100",
        key_path="/home/user/.ssh/id_rsa",
    )
    io = SSHProcessIO(start_command="python app.py", ssh_config=config)

    with patch("blabot.ssh_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.expect.side_effect = pexpect.TIMEOUT("timeout")
        mock_spawn.return_value = mock_process

        with pytest.raises(RuntimeError, match="Failed to login"):
            io.start()
