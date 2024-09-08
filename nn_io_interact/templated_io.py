from abc import ABC
from abc import abstractmethod


class TemplatedIO(ABC):
    """
    This class provides the ability to exchange input and output with other processes.

    This class is assumed to be inherited.
    Some methods should be implemented by the inheritor in a form suitable for the target.
    """

    def __init__(self, prompt: str = None, newline: str = None):
        self.process = None
        self.prompt = prompt
        self.newline = newline

    @abstractmethod
    def start(self):
        """
        This is the method used to initiate an incoming/outgoing call to/from a process

        This method should be implemented by the inheritor in a form suitable for the target.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        This is the method used to terminate the process.

        This method should be implemented by the inheritor in a form suitable for the target.
        """
        pass

    @abstractmethod
    def send_command(self, command) -> None:
        """
        This is the method used to send the string to the process.

        This method should be implemented by the inheritor in a form suitable for the target.
        """
        pass

    @abstractmethod
    def wait_for(self, expect, timeout_sec: float = 3.0) -> str:
        """
        This method is used to wait for the expected string to arrive from the process.

        This method should be implemented by the inheritor in a form suitable for the target.
        """
        pass

    def restart(self):
        self.stop()
        self.start()

    def run_command(
            self,
            command: str = "",
            expect: str = "",
            timeout_sec: float = 0.2,
            attempts: int = 1) -> str:

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
        if self.prompt is None:
            return True

        first_timeout = 0.5
        res = self.wait_for(self.prompt, first_timeout)
        if res == self.prompt:
            return True

        # Send a new line and try again
        self.send_command("")
        res = self.wait_for(self.prompt, timeout_sec)
        return res == self.prompt
