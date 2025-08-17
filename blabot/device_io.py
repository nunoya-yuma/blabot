"""Serial device communication implementation using pexpect_serial.

This module provides DeviceIO class that implements the TemplatedIO interface
for communicating with serial devices such as USB-to-serial adapters.
"""

import sys

import pexpect
import serial
from pexpect_serial import SerialSpawn

from .templated_io import TemplatedIO


class DeviceIO(TemplatedIO):
    """Serial device communication using pexpect_serial.

    Implements the TemplatedIO interface for communicating with serial devices
    such as USB-to-serial adapters. Uses pyserial for device connection and
    pexpect_serial for interaction.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        """Initialize DeviceIO instance.

        Args:
            port: Serial port path (e.g., '/dev/ttyUSB0', 'COM1').
            baudrate: Serial communication speed in bits per second.
            prompt: Expected prompt string to wait for.
            newline: Newline character to append to commands.

        """
        super().__init__(prompt, newline)
        self.process: SerialSpawn | None = None
        self.device = serial.Serial(port, baudrate, timeout=1)

    def start(self) -> None:
        """Start serial device communication.

        Opens the serial port if not already open and creates a SerialSpawn
        instance for pexpect-style interaction.

        Raises:
            RuntimeError: If communication is already started.

        """
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        if not self.device.is_open:
            self.device.open()

        self.process = SerialSpawn(self.device)
        self.process.logfile = sys.stdout.buffer

    def stop(self) -> None:
        """Stop serial device communication.

        Closes the SerialSpawn instance and the underlying serial port.
        Cleans up the process reference.

        Raises:
            RuntimeError: If communication is not started or port is closed.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        if not self.device.is_open:
            msg = "Device port is already closed"
            raise RuntimeError(msg)

        self.process.close()
        self.device.close()
        self.process = None

    def send_command(self, command: str) -> None:
        """Send a command to the serial device.

        Appends the configured newline character and sends the command
        to the device.

        Args:
            command: Command string to send.

        Raises:
            RuntimeError: If communication is not started.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        output_line = command + self._newline
        self.process.sendline(output_line)

    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str | None:
        """Wait for expected pattern from the serial device.

        Uses pexpect to wait for the specified pattern to appear in the
        device output stream.

        Args:
            expect: Regular expression pattern to wait for.
            timeout_sec: Maximum time to wait in seconds.

        Returns:
            str: The matched string if pattern is found.
            None: If timeout occurs before pattern is matched.

        Raises:
            RuntimeError: If communication is not started.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        expect_list = [
            pexpect.TIMEOUT,
        ]
        expect_list.append(expect)
        index = self.process.expect(expect_list, timeout=timeout_sec)

        match = None
        if index == 0:
            # pexpect.TIMEOUT is output
            # This means that no matching string was output until the timeout.
            pass
        else:
            match = self.process.after.decode("utf-8")

        return match
