"""Local process communication implementation using pexpect.

This module provides ProcessIO class that implements the TemplatedIO interface
for communicating with local processes using the pexpect library.
"""

import sys

import pexpect

from .templated_io import TemplatedIO


class ProcessIO(TemplatedIO):
    """Local process communication using pexpect.

    Implements the TemplatedIO interface for communicating with local processes
    using the pexpect library. Handles process startup, command execution,
    and output parsing for command-line applications.
    """

    def __init__(
        self,
        start_command: str,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        """Initialize ProcessIO instance.

        Args:
            start_command: Command to start the target process.
            prompt: Expected prompt string to wait for.
            newline: Newline character to append to commands.

        """
        super().__init__(prompt, newline)
        self.process: pexpect.spawn | None = None
        self._start_command = start_command

    def start(self) -> None:
        """Start the local process using pexpect.

        Spawns the configured command as a new process and sets up
        logging to stdout.

        Raises:
            RuntimeError: If process is already started.

        """
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        self.process = pexpect.spawn(self._start_command)
        self.process.logfile = sys.stdout.buffer

    def stop(self) -> None:
        """Stop the local process.

        Terminates the running process and waits for it to exit.
        Cleans up the process reference.

        Raises:
            RuntimeError: If process is not started.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        self.process.terminate()
        self.process.wait()
        self.process = None

    def send_command(self, command: str) -> None:
        """Send a command to the process.

        Appends the configured newline character and sends the command
        to the process stdin.

        Args:
            command: Command string to send.

        Raises:
            RuntimeError: If process is not started.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        output_line = command + self._newline
        self.process.sendline(output_line)

    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str | None:
        """Wait for expected pattern in process output.

        Uses pexpect to wait for the specified pattern to appear in the
        process output stream.

        Args:
            expect: Regular expression pattern to wait for.
            timeout_sec: Maximum time to wait in seconds.

        Returns:
            str: The matched string if pattern is found.
            None: If timeout occurs before pattern is matched.

        Raises:
            RuntimeError: If process is not started.
            TypeError: If the matched output is not bytes.

        """
        if not self.process:
            msg = "Process not started"
            raise RuntimeError(msg)

        try:
            self.process.expect(expect, timeout=timeout_sec)
        except pexpect.TIMEOUT:
            return None

        if not isinstance(self.process.after, bytes):
            err_msg = "Expected bytes from process.after"
            raise TypeError(err_msg)

        return self.process.after.decode("utf-8")
