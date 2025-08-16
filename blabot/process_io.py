import sys

import pexpect

from .templated_io import TemplatedIO


class ProcessIO(TemplatedIO):
    """
    This class provides the ability to exchange input and output
    with other processes in the same machine.

    This class inherits from TemplatedIO class and implements
    the necessary methods so that it can actually communicate
    with the target process.
    This class uses `pexpect` to manage startup and input/output.
    This class itself only interacts with processes in the same machine,
    but may be applied to other targets by generating other classes that
    inherit from this class.
    """

    def __init__(
        self,
        start_command: str,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        super().__init__(prompt, newline)
        self._start_command = start_command

    def start(self) -> None:
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        self.process = pexpect.spawn(self._start_command)
        self.process.logfile = sys.stdout.buffer

    def stop(self) -> None:
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        self.process.terminate()
        self.process.wait()
        self.process = None

    def send_command(self, command: str) -> None:
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
