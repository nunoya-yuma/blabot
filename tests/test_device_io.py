"""Unit tests for DeviceIO class."""

from unittest.mock import MagicMock, patch

import pexpect
import pytest

from blabot.device_io import DeviceIO

# =============================================================================
# start() tests
# =============================================================================


@pytest.mark.unit
def test_start_creates_serial_spawn():
    """start() should create SerialSpawn with the device."""
    with patch("blabot.device_io.serial.Serial") as mock_serial_class:
        mock_device = MagicMock()
        mock_device.is_open = True
        mock_serial_class.return_value = mock_device

        io = DeviceIO(port="/dev/ttyUSB0", baudrate=115200)

        with patch("blabot.device_io.SerialSpawn") as mock_spawn_class:
            mock_spawn = MagicMock()
            mock_spawn_class.return_value = mock_spawn

            io.start()

            mock_spawn_class.assert_called_once_with(mock_device)
            assert io.process is mock_spawn


@pytest.mark.unit
def test_start_opens_device_if_closed():
    """start() should open device if it's not already open."""
    with patch("blabot.device_io.serial.Serial") as mock_serial_class:
        mock_device = MagicMock()
        mock_device.is_open = False
        mock_serial_class.return_value = mock_device

        io = DeviceIO(port="/dev/ttyUSB0", baudrate=115200)

        with patch("blabot.device_io.SerialSpawn"):
            io.start()

            mock_device.open.assert_called_once()


# =============================================================================
# stop() tests
# =============================================================================


@pytest.mark.unit
def test_stop_closes_process_and_device():
    """stop() should close both SerialSpawn and serial device."""
    with patch("blabot.device_io.serial.Serial") as mock_serial_class:
        mock_device = MagicMock()
        mock_device.is_open = True
        mock_serial_class.return_value = mock_device

        io = DeviceIO(port="/dev/ttyUSB0")
        mock_process = MagicMock()
        io.process = mock_process

        io.stop()

        mock_process.close.assert_called_once()
        mock_device.close.assert_called_once()
        assert io.process is None


# =============================================================================
# send_command() tests
# =============================================================================


@pytest.mark.unit
def test_send_command_sends_with_newline():
    """send_command() should append newline and send via sendline()."""
    with patch("blabot.device_io.serial.Serial"):
        io = DeviceIO(port="/dev/ttyUSB0", newline="\r\n")
        mock_process = MagicMock()
        io.process = mock_process

        io.send_command("AT")

        mock_process.sendline.assert_called_once_with("AT\r\n")


# =============================================================================
# wait_for() tests
# =============================================================================


@pytest.mark.unit
def test_wait_for_returns_match_when_found():
    """wait_for() should return matched string when pattern is found."""
    with patch("blabot.device_io.serial.Serial"):
        io = DeviceIO(port="/dev/ttyUSB0")
        mock_process = MagicMock()
        mock_process.after = b"OK"
        io.process = mock_process

        result = io.wait_for("OK", timeout_sec=1.0)

        assert result == "OK"


@pytest.mark.unit
def test_wait_for_returns_none_on_timeout():
    """wait_for() should return None when pexpect.TIMEOUT is raised."""
    with patch("blabot.device_io.serial.Serial"):
        io = DeviceIO(port="/dev/ttyUSB0")
        mock_process = MagicMock()
        mock_process.expect.side_effect = pexpect.TIMEOUT("timeout")
        io.process = mock_process

        result = io.wait_for("OK", timeout_sec=1.0)

        assert result is None
