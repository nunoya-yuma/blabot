"""Docker container process communication implementation.

Provides classes for communicating with processes inside Docker containers
from the host PC. Includes DockerRunIO for creating new containers with
'docker run' and DockerExecIO for executing commands in existing containers
with 'docker exec'. Choose the appropriate class for your use case.
"""

import subprocess
import sys
from dataclasses import dataclass

import pexpect

from .process_io import ProcessIO


@dataclass
class DockerRunConfig:
    """Configuration for Docker run command parameters."""

    image_name: str
    container_name: str
    remove_container: bool = True


@dataclass
class DockerExecConfig:
    """Configuration for Docker exec command parameters."""

    container_name: str
    remove_container: bool = True


class DockerIOBase(ProcessIO):
    """Base class for Docker container process communication.

    Provides common functionality shared between DockerRunIO and DockerExecIO.
    This class is intended for internal use only and should not be used directly.
    """

    def _start_docker_and_process(self, docker_activate_command: str) -> None:
        """Start Docker container and initialize process communication.

        Args:
            docker_activate_command: Docker command to execute.

        Raises:
            RuntimeError: If Docker container fails to start.

        """
        self.process = pexpect.spawn(docker_activate_command)
        self.process.logfile = sys.stdout.buffer

        # Wait for login to complete
        if not self.wait_for(r"#"):
            msg = "Failed to start docker"
            raise RuntimeError(msg)

        # Do not use `run_command` method here.
        # For example, if "> " is assigned to the self.prompt,
        # the log immediately after login does not contain this.
        # This self.prompt is for test target process.
        self.send_command(self._start_command)


class DockerRunIO(DockerIOBase):
    """Docker container process communication using 'docker run'.

    Creates and manages Docker containers using 'docker run' command.
    Automatically handles container lifecycle including creation and cleanup.
    Use DockerExecIO for pre-existing containers.
    """

    def __init__(
        self,
        start_command: str,
        docker_run_config: DockerRunConfig,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        """Initialize DockerRunIO instance.

        Args:
            start_command: Command to execute in the container.
            docker_run_config: Docker run configuration.
            prompt: Expected prompt string to wait for.
            newline: Newline character to append to commands.

        """
        super().__init__(start_command, prompt, newline)
        self._docker_image_name = docker_run_config.image_name
        self._docker_container_name = docker_run_config.container_name
        self._remove_container = docker_run_config.remove_container

    def start(self) -> None:
        """Start Docker container and process communication.

        Creates a new Docker container using 'docker run' and starts
        the configured command inside it.

        Raises:
            RuntimeError: If process is already started or container fails to start.

        """
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        docker_run_command = self._build_command()
        self._start_docker_and_process(docker_run_command)

    def _build_command(self) -> str:
        """Build the docker run command string.

        Returns:
            Complete docker run command with configured options.

        """
        docker_run_command = "docker run -it"
        if self._remove_container:
            docker_run_command += " --rm"

        if self._docker_container_name:
            docker_run_command += f" --name {self._docker_container_name}"

        # e.g.) docker run -it --rm --name test_container
        # ghcr.io/nunoya-yuma/blabot/example-app:latest bash
        docker_run_command += f" {self._docker_image_name} bash"

        return docker_run_command


class DockerExecIO(DockerIOBase):
    """Docker container process communication using 'docker exec'.

    Executes commands in existing Docker containers using 'docker exec'.
    Requires the target container to be running before use.
    """

    def __init__(
        self,
        start_command: str,
        docker_exec_config: DockerExecConfig,
        prompt: str = "",
        newline: str = "",
    ) -> None:
        """Initialize DockerExecIO instance.

        Args:
            start_command: Command to execute in the container.
            docker_exec_config: Docker exec configuration.
            prompt: Expected prompt string to wait for.
            newline: Newline character to append to commands.

        """
        super().__init__(start_command, prompt, newline)
        self._docker_container_name = docker_exec_config.container_name
        self._remove_container = docker_exec_config.remove_container

    def start(self) -> None:
        """Start process communication with existing Docker container.

        Executes 'docker exec' to connect to the running container.

        Raises:
            RuntimeError: If process is already started or container connection fails.

        """
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        docker_exec_command = f"docker exec -it {self._docker_container_name} bash"
        self._start_docker_and_process(docker_exec_command)

    def stop(self) -> None:
        """Stop process communication and optionally remove container.

        Stops the process communication and removes the container if configured.

        Raises:
            RuntimeError: If container name is lost or removal fails.

        """
        super().stop()

        if not self._remove_container:
            return

        if not self._docker_container_name:
            msg = "Container name is lost"
            raise RuntimeError(msg)

        docker_remove_command = ["docker", "rm", "-f", self._docker_container_name]
        res_remove = subprocess.run(
            docker_remove_command,
            check=False,
            stdout=subprocess.DEVNULL,
        )
        if res_remove.returncode != 0:
            msg = f"Failed to remove docker container '{self._docker_container_name}'"
            raise RuntimeError(msg)
