from abc import ABC
from abc import abstractmethod


class TemplatedIO(ABC):
    """
    This class provides the ability to exchange input
    and output with other processes.

    This class is assumed to be inherited.
    Some methods should be implemented by the inheritor in a form suitable
    for the target.
    """

    def __init__(self, prompt: str = "", newline: str = ""):
        self.process = None
        self._prompt = prompt
        self._newline = newline

    @abstractmethod
    def start(self):
        """
        This is the method used to initiate an incoming/outgoing call
        to/from a process

        This method should be implemented by the inheritor in a form suitable
        for the target.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        This is the method used to terminate the process.

        This method should be implemented by the inheritor in a form suitable
        for the target.
        """
        pass

    @abstractmethod
    def send_command(self, command: str) -> None:
        """
        This is the method used to send the string to the process.

        This method should be implemented by the inheritor in a form suitable
        for the target.
        """
        pass

    @abstractmethod
    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str:
        """
        This method is used to wait for the expected string to arrive
        from the process.

        This method should be implemented by the inheritor in a form suitable
        for the target.
        """
        pass

    def restart(self):
        self.stop()
        self.start()

    def run_command(
            self,
            command: str,
            expect: str = "",
            timeout_sec: float = 0.2,
            attempts: int = 1) -> str:
        """
        This is the method used to send the string to the process and wait
        for expected string

        This method waits for a prompt and then sends the command.
        If the expected string is returned, an object containing
        the string is returned.

        If the expected string is not included, the string is not consumed
        and will be parsed again at the next opportunity.
        If you want to prevent this, use the `wait_and_consume_logs` method.
        """

        if not self.process:
            raise RuntimeError("Process not started")

        if self.wait_for_prompt() is False:
            raise Exception("Prompt does not appear")

        for _ in range(attempts):
            self.send_command(command)
            match = self.wait_for(expect, timeout_sec=timeout_sec)
            if match is not None:
                break

        return match

    def wait_for_prompt(self, timeout_sec: float = 3.0) -> bool:
        # If prompt is not set, ignore it
        if self._prompt is None:
            return True

        FIRST_TIMEOUT_SEC = 0.5
        res = self.wait_for(self._prompt, FIRST_TIMEOUT_SEC)
        if res == self._prompt:
            return True

        # Send a new line and try again
        self.send_command(self._newline)
        res = self.wait_for(self._prompt, timeout_sec)
        return res == self._prompt

    def wait_and_consume_logs(self, timeout_sec: float = 3.0) -> None:
        self.wait_for(".*", timeout_sec)
