import pexpect
import sys

from .process_io import ProcessIO


class SSHProcessIO(ProcessIO):
    def __init__(
            self,
            start_command: str,
            user_name: str,
            host_name: str,
            key_path: str,
            prompt: str = "",
            newline: str = ""
    ):

        super().__init__(start_command, prompt, newline)
        self._user_name = user_name
        self._host_name = host_name
        self._key_path = key_path

    def start(self):
        if self.process:
            raise RuntimeError("Process has already started")

        ssh_login_cmd = (
            f"ssh -i {self._key_path} {self._user_name}@{self._host_name}")
        self.process = pexpect.spawn(ssh_login_cmd)
        self.process.logfile = sys.stdout.buffer

        # Wait for login to complete
        assert self.wait_for(r"\$", 15), "Failed to login"

        # Do not use `run_command` method here.
        # For example, if "> " is assigned to the self.prompt,
        # the log immediately after login does not contain this.
        # This self.prompt is for test target process.
        self.send_command(self._start_command)
