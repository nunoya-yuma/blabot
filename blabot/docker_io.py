"""
This module provides the ability to exchange input and output
with other processes in the docker container

This module controls the input/output of processes in the container
from the host PC.
To realize this function, `DockerRunIO` using `docker run` command and
`DockerExecIO` using `docker exec` command are available.
Please use the appropriate class for your purpose.
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
    """
    This class has parts in common with other classes in the same module.

    In this module, there are classes `DockerRunIO` and `DockerExecIO`.
    If there are common parts among them, this class will hold them
    and share them by inheritance.
    This class is intended to be used only within this module
    and is not intended to be used externally.
    """

    def _start_docker_and_process(self, docker_activate_command: str):
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
    """
    This class provides the ability to exchange input and output
    with other processes in the docker container using `docker run` command.

    This class controls the input/output of processes in the container
    from the host PC.
    Although a docker image must be available on the host PC,
    this class also has the ability to automatically launch containers.
    If you need to work in the container in advance, use `DockerExecIO` class.
    """

    def __init__(
        self,
        start_command: str,
        docker_run_config: DockerRunConfig,
        prompt: str = "",
        newline: str = "",
    ):
        super().__init__(start_command, prompt, newline)
        self._docker_image_name = docker_run_config.image_name
        self._docker_container_name = docker_run_config.container_name
        self._remove_container = docker_run_config.remove_container

    def start(self):
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        docker_run_command = self._build_command()
        self._start_docker_and_process(docker_run_command)

    def _build_command(self):
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
    """
    This class provides the ability to exchange input and output
    with other processes in the docker container using `docker exec` command.

    This class controls the input/output of processes in the container
    from the host PC.
    Also, this class assumes that the container is running in advance,
    so please start it before using this class.
    """

    def __init__(
        self,
        start_command: str,
        docker_exec_config: DockerExecConfig,
        prompt: str = "",
        newline: str = "",
    ):
        super().__init__(start_command, prompt, newline)
        self._docker_container_name = docker_exec_config.container_name
        self._remove_container = docker_exec_config.remove_container

    def start(self):
        if self.process:
            msg = "Process has already started"
            raise RuntimeError(msg)

        docker_exec_command = f"docker exec -it {self._docker_container_name} bash"
        self._start_docker_and_process(docker_exec_command)

    def stop(self):
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
