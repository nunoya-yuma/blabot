"""blabot: A Python library for automated CLI testing and process interaction.

This library provides a unified interface for communicating with processes
across different environments including local processes, SSH connections,
serial devices, and Docker containers.
"""

from importlib.metadata import version

from .device_io import DeviceIO
from .docker_io import DockerExecConfig, DockerExecIO, DockerRunConfig, DockerRunIO
from .process_io import ProcessIO
from .ssh_io import SSHConfig, SSHProcessIO
from .templated_io import TemplatedIO

__version__ = version("blabot")
__all__ = [
    "DeviceIO",
    "DockerExecConfig",
    "DockerExecIO",
    "DockerRunConfig",
    "DockerRunIO",
    "ProcessIO",
    "SSHConfig",
    "SSHProcessIO",
    "TemplatedIO",
]
