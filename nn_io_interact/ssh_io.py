from . import program_io
import pexpect
import sys


class SSHProcessIO(program_io.ProgramIO):
    def __init__(
            self,
            user_name: str = "",
            host_name: str = "",
            key_path: str = "",
            start_command: str = ""):

        if user_name == "" or host_name == "" or key_path == "":
            raise ValueError("Input is empty")

        super().__init__(start_command=start_command)
        self.user_name = user_name
        self.host_name = host_name
        self.key_path = key_path

    def start(self):
        if self.process:
            raise RuntimeError("Process has already started")

        ssh_login_cmd = f"ssh -i {self.key_path} {self.user_name}@{self.host_name}"
        self.process = pexpect.spawn(ssh_login_cmd)
        self.process.logfile = sys.stdout.buffer

        # Wait for login to complete
        assert self.wait_for(r"\$", 15), "Failed to login"

        # Do not use `run_command` method here.
        # For example, if "> " is assigned to the self.prompt, the log immediately
        # after login does not contain this.
        # This self.prompt is for test target process.
        self.send_command(self.start_command)
