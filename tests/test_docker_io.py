"""Unit tests for DockerRunIO and DockerExecIO classes."""

from unittest.mock import MagicMock, patch

import pexpect
import pytest

from blabot.docker_io import (
    DockerExecConfig,
    DockerExecIO,
    DockerRunConfig,
    DockerRunIO,
)

# =============================================================================
# DockerRunIO.start() tests
# =============================================================================


@pytest.mark.unit
def test_docker_run_start_spawns_with_correct_command():
    """start() should spawn docker run command and send start_command."""
    config = DockerRunConfig(
        image_name="myimage:latest",
        container_name="mycontainer",
    )
    io = DockerRunIO(
        start_command="python app.py",
        docker_run_config=config,
        newline="\n",
    )

    with patch("blabot.docker_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.after = b"#"
        mock_spawn.return_value = mock_process

        io.start()

        mock_spawn.assert_called_once_with(
            "docker run -it --rm --name mycontainer myimage:latest bash"
        )
        mock_process.sendline.assert_called_with("python app.py\n")


@pytest.mark.unit
def test_docker_run_start_raises_when_docker_fails():
    """start() should raise RuntimeError when docker container fails to start."""
    config = DockerRunConfig(
        image_name="myimage:latest",
        container_name="mycontainer",
    )
    io = DockerRunIO(start_command="python app.py", docker_run_config=config)

    with patch("blabot.docker_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.expect.side_effect = pexpect.TIMEOUT("timeout")
        mock_spawn.return_value = mock_process

        with pytest.raises(RuntimeError, match="Failed to start docker"):
            io.start()


@pytest.mark.unit
def test_docker_run_start_without_rm():
    """start() should not include --rm when remove_container is False."""
    config = DockerRunConfig(
        image_name="myimage:latest",
        container_name="mycontainer",
        remove_container=False,
    )
    io = DockerRunIO(start_command="python app.py", docker_run_config=config)

    with patch("blabot.docker_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.after = b"#"
        mock_spawn.return_value = mock_process

        io.start()

        mock_spawn.assert_called_once_with(
            "docker run -it --name mycontainer myimage:latest bash"
        )


# =============================================================================
# DockerExecIO.start() tests
# =============================================================================


@pytest.mark.unit
def test_docker_exec_start_spawns_with_correct_command():
    """start() should spawn docker exec command."""
    config = DockerExecConfig(container_name="mycontainer")
    io = DockerExecIO(
        start_command="python app.py",
        docker_exec_config=config,
        newline="\n",
    )

    with patch("blabot.docker_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.after = b"#"
        mock_spawn.return_value = mock_process

        io.start()

        mock_spawn.assert_called_once_with("docker exec -it mycontainer bash")


@pytest.mark.unit
def test_docker_exec_start_raises_when_docker_fails():
    """start() should raise RuntimeError when docker exec fails."""
    config = DockerExecConfig(container_name="mycontainer")
    io = DockerExecIO(start_command="python app.py", docker_exec_config=config)

    with patch("blabot.docker_io.pexpect.spawn") as mock_spawn:
        mock_process = MagicMock()
        mock_process.expect.side_effect = pexpect.TIMEOUT("timeout")
        mock_spawn.return_value = mock_process

        with pytest.raises(RuntimeError, match="Failed to start docker"):
            io.start()


# =============================================================================
# DockerExecIO.stop() tests
# =============================================================================


@pytest.mark.unit
def test_docker_exec_stop_removes_container():
    """stop() should call subprocess.run to remove container."""
    config = DockerExecConfig(container_name="mycontainer", remove_container=True)
    io = DockerExecIO(start_command="python app.py", docker_exec_config=config)

    mock_process = MagicMock()
    io.process = mock_process

    with patch("blabot.docker_io.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        io.stop()

        mock_process.terminate.assert_called_once()
        mock_run.assert_called_once()
        # Verify container removal command
        call_args = mock_run.call_args
        assert call_args[0][0] == ["docker", "rm", "-f", "mycontainer"]


@pytest.mark.unit
def test_docker_exec_stop_skips_removal_when_disabled():
    """stop() should not remove container when remove_container is False."""
    config = DockerExecConfig(container_name="mycontainer", remove_container=False)
    io = DockerExecIO(start_command="python app.py", docker_exec_config=config)

    mock_process = MagicMock()
    io.process = mock_process

    with patch("blabot.docker_io.subprocess.run") as mock_run:
        io.stop()

        mock_process.terminate.assert_called_once()
        mock_run.assert_not_called()


@pytest.mark.unit
def test_docker_exec_stop_raises_when_removal_fails():
    """stop() should raise RuntimeError when container removal fails."""
    config = DockerExecConfig(container_name="mycontainer", remove_container=True)
    io = DockerExecIO(start_command="python app.py", docker_exec_config=config)

    mock_process = MagicMock()
    io.process = mock_process

    with patch("blabot.docker_io.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1)  # Removal failed

        with pytest.raises(RuntimeError, match="Failed to remove docker container"):
            io.stop()
