import pexpect
import sys

from .process_io import ProcessIO


class DockerProcessIO(ProcessIO):
    """
    This class provides the ability to exchange input and output
    with other processes in the docker container

    This class controls the input/output of processes in the container from the host PC.
    Although a docker image must be available on the host PC, this class also has the ability to
    automatically launch containers.
    If you need to work in the container in advance, do it and detach from the container so that
    this class can resume it with the docker exec command and set the use_docker_exec argument to
    False.
    """

    def __init__(
            self,
            start_command: str,
            docker_image_name: str,
            docker_container_name: str = "",
            use_docker_exec: bool = False,
            prompt: str = "",
            newline: str = ""
    ):
        if use_docker_exec and docker_container_name == "":
            raise ValueError("If use_docker_exec is True, docker_container_name must be passed")

        super().__init__(start_command, prompt, newline)
        self.docker_image_name = docker_image_name
        self.docker_container_name = docker_container_name
        self.use_docker_exec = use_docker_exec

    def start(self):
        if self.process:
            raise RuntimeError("Process has already started")

        spawn_command = ""

        if self.use_docker_exec:
            docker_exec_command = f"docker exec -it {self.docker_container_name} bash"
            spawn_command = docker_exec_command
        else:
            docker_run_command = "docker run -it --rm"
            if self.docker_container_name:
                docker_run_command += f" --name {self.docker_container_name}"

            docker_run_command += f" {self.docker_image_name} bash"
            # e.g.) docker run -it --rm --name testtest nn/iointeract:1.0 bash
            spawn_command = docker_run_command

        self.process = pexpect.spawn(spawn_command)
        self.process.logfile = sys.stdout.buffer

        # Wait for login to complete
        assert self.wait_for(r"#"), "Failed to start docker"

        # Do not use `run_command` method here.
        # For example, if "> " is assigned to the self.prompt, the log immediately
        # after login does not contain this.
        # This self.prompt is for test target process.
        self.send_command(self.start_command)
