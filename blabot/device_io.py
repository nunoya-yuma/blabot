import sys

import pexpect
import serial
from pexpect_serial import SerialSpawn

from .templated_io import TemplatedIO


class DeviceIO(TemplatedIO):
    """
    This class provides the ability to exchange input and output
    with other device(e.g. /dev/ttyUSB0).

    This class inherits from TemplatedIO class and implements the necessary
    methods so that it can actually communicate with the target device.
    This class uses `pexpect` to manage startup and input/output.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        super().__init__(prompt, newline)
        self.device = serial.Serial(port, baudrate, timeout=1)

    def start(self) -> None:
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        if not self.device.is_open:
            self.device.open()

        self.process = SerialSpawn(self.device)
        self.process.logfile = sys.stdout.buffer

    def stop(self) -> None:
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
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        output_line = command + self._newline
        self.process.sendline(output_line)

    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str | None:
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
