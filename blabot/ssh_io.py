"""SSH process communication implementation using pexpect.

This module provides SSHProcessIO class that implements the TemplatedIO interface
for communicating with processes on remote machines via SSH connections.
"""

import sys
from dataclasses import dataclass

import pexpect

from .process_io import ProcessIO


@dataclass
class SSHConfig:
    """Configuration for SSH connection parameters."""

    user_name: str
    host_name: str
    key_path: str


class SSHProcessIO(ProcessIO):
    """SSH-based process communication using pexpect.

    Extends ProcessIO to communicate with processes on remote machines
    via SSH connections. Handles SSH login and command execution.
    """

    def __init__(
        self,
        start_command: str,
        ssh_config: SSHConfig,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        """Initialize SSHProcessIO instance.

        Args:
            start_command: Command to execute on the remote machine.
            ssh_config: SSH connection configuration.
            prompt: Expected prompt string to wait for.
            newline: Newline character to append to commands.

        """
        super().__init__(start_command, prompt, newline)
        self._user_name = ssh_config.user_name
        self._host_name = ssh_config.host_name
        self._key_path = ssh_config.key_path

    def start(self) -> None:
        """Start SSH connection and remote process.

        Establishes SSH connection to the remote host, waits for login
        completion, then starts the configured command on the remote machine.

        Raises:
            RuntimeError: If process is already started or SSH login fails.

        """
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        ssh_login_cmd = f"ssh -i {self._key_path} {self._user_name}@{self._host_name}"
        self.process = pexpect.spawn(ssh_login_cmd)
        self.process.logfile = sys.stdout.buffer

        # Wait for login to complete
        if not self.wait_for(r"\$", 15):
            msg = "Failed to login"
            raise RuntimeError(msg)

        # Do not use `run_command` method here.
        # For example, if "> " is assigned to the self.prompt,
        # the log immediately after login does not contain this.
        # This self.prompt is for test target process.
        self.send_command(self._start_command)
