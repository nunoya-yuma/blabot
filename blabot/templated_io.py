"""Abstract base class for process communication interfaces.

This module provides the core abstraction for communicating with processes
across different environments (local, SSH, Docker, serial devices).
"""

from abc import ABC, abstractmethod


class TemplatedIO(ABC):
    """Abstract base class for process communication.

    Provides a unified interface for exchanging input and output with processes
    across different environments. This class is designed to be inherited by
    concrete implementations for specific process types.
    """

    def __init__(self, prompt: str = "", newline: str = "") -> None:
        """Initialize the TemplatedIO instance.

        Args:
            prompt: Expected prompt string to wait for before sending commands.
            newline: Newline character to append to commands.

        """
        self._prompt = prompt
        self._newline = newline

    @abstractmethod
    def start(self) -> None:
        """Start the process communication.

        Initiate communication with the target process. This method must be
        implemented by subclasses according to their specific process type.
        """

    @abstractmethod
    def stop(self) -> None:
        """Stop the process communication.

        Terminate communication with the target process. This method must be
        implemented by subclasses according to their specific process type.
        """

    @abstractmethod
    def send_command(self, command: str) -> None:
        """Send a command string to the process.

        This method must be implemented by subclasses according to their
        specific process communication mechanism.
        """

    @abstractmethod
    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str | None:
        """Wait for expected string from the process.

        Wait for the specified pattern to appear in the process output.
        This method must be implemented by subclasses according to their
        specific process communication mechanism.

        Args:
            expect: Regular expression pattern to wait for.
            timeout_sec: Maximum time to wait in seconds.

        Returns:
            str: The matched string if expected pattern is found.
            None: If timeout occurs before pattern is matched.

        """

    def restart(self) -> None:
        """Restart the process by stopping and starting it again."""
        self.stop()
        self.start()

    def run_command(
        self,
        command: str,
        expect: str = "",
        timeout_sec: float = 0.2,
        attempts: int = 1,
    ) -> str | None:
        """Send command and wait for expected response.

        Wait for a prompt, send the command, and wait for the expected response.
        If the expected string is not found, it remains in the buffer for the
        next operation. Use `wait_and_consume_logs` to clear the buffer if needed.

        Args:
            command: Command string to send.
            expect: Expected response pattern to wait for.
            timeout_sec: Maximum time to wait for response.
            attempts: Number of retry attempts.

        Returns:
            str: The matched string if expected pattern is found.
            None: If timeout occurs or pattern not matched after all attempts.

        """
        if self.wait_for_prompt() is False:
            msg = "Prompt does not appear"
            raise RuntimeError(msg)

        for _ in range(attempts):
            self.send_command(command)
            match = self.wait_for(expect, timeout_sec=timeout_sec)
            if match is not None:
                break

        return match

    def wait_for_prompt(self, timeout_sec: float = 3.0) -> bool:
        """Wait for the configured prompt to appear.

        Args:
            timeout_sec: Maximum time to wait for the prompt.

        Returns:
            True if prompt appears within timeout, False otherwise.

        """
        # If prompt is not set, ignore it
        if self._prompt is None:
            return True

        first_timeout_sec = 0.5
        res = self.wait_for(self._prompt, first_timeout_sec)
        if res == self._prompt:
            return True

        # Send a new line and try again
        self.send_command(self._newline)
        res = self.wait_for(self._prompt, timeout_sec)
        return res == self._prompt

    def wait_and_consume_logs(self, timeout_sec: float = 3.0) -> None:
        """Wait and consume any pending log output.

        This method is useful for clearing the output buffer before sending
        new commands to avoid parsing stale output.

        Args:
            timeout_sec: Maximum time to wait for output.

        """
        self.wait_for(".*", timeout_sec)
