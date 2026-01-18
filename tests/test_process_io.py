"""Unit tests for ProcessIO class."""

from unittest.mock import MagicMock, patch

import pytest

from blabot.process_io import ProcessIO

# =============================================================================
# start() tests
# =============================================================================


@pytest.mark.unit
def test_start_spawns_process():
    """start() should spawn a new process with the configured command."""
    io = ProcessIO(start_command="python app.py", prompt=">>> ", newline="\n")

    with patch("blabot.process_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_spawn.return_value = mock_process

        io.start()

        mock_spawn.assert_called_once_with("python app.py")
        assert io.process is mock_process


# =============================================================================
# stop() tests
# =============================================================================


@pytest.mark.unit
def test_stop_terminates_process():
    """stop() should terminate the process and wait for exit."""
    io = ProcessIO(start_command="python app.py")
    mock_process = MagicMock()
    io.process = mock_process

    io.stop()

    mock_process.terminate.assert_called_once()
    mock_process.wait.assert_called_once()
    assert io.process is None


# =============================================================================
# send_command() tests
# =============================================================================


@pytest.mark.unit
def test_send_command_sends_with_newline():
    """send_command() should append newline and send via sendline()."""
    io = ProcessIO(start_command="python app.py", newline="\n")
    mock_process = MagicMock()
    io.process = mock_process

    io.send_command("ls -la")

    mock_process.sendline.assert_called_once_with("ls -la\n")


# =============================================================================
# wait_for() tests
# =============================================================================


@pytest.mark.unit
def test_wait_for_returns_match_when_found():
    """wait_for() should return matched string when pattern is found."""
    io = ProcessIO(start_command="python app.py")
    mock_process = MagicMock()
    mock_process.expect.return_value = 1  # Index 1 = pattern matched
    mock_process.after = b"expected"
    io.process = mock_process

    result = io.wait_for("expected", timeout_sec=1.0)

    assert result == "expected"


@pytest.mark.unit
def test_wait_for_returns_none_on_timeout():
    """wait_for() should return None when timeout occurs."""
    io = ProcessIO(start_command="python app.py")
    mock_process = MagicMock()
    mock_process.expect.return_value = 0  # Index 0 = TIMEOUT
    io.process = mock_process

    result = io.wait_for("expected", timeout_sec=1.0)

    assert result is None
