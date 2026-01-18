"""Unit tests for TemplatedIO class."""

import pytest

from blabot.templated_io import TemplatedIO


class StubIO(TemplatedIO):
    """Stub implementation of TemplatedIO for testing.

    Records method calls and returns pre-configured responses.
    """

    def __init__(self, prompt: str = "", newline: str = "") -> None:
        super().__init__(prompt, newline)
        self.call_history: list[str] = []
        self.commands_sent: list[str] = []
        self.wait_for_responses: list[str | None] = []
        self._wait_for_call_index = 0

    def start(self) -> None:
        self.call_history.append("start")

    def stop(self) -> None:
        self.call_history.append("stop")

    def send_command(self, command: str) -> None:
        self.commands_sent.append(command)
        self.call_history.append(f"send_command:{command}")

    def wait_for(self, expect: str, timeout_sec: float = 3.0) -> str | None:  # noqa: ARG002
        self.call_history.append(f"wait_for:{expect}")
        if self._wait_for_call_index < len(self.wait_for_responses):
            response = self.wait_for_responses[self._wait_for_call_index]
            self._wait_for_call_index += 1
            return response
        return None

    def set_wait_for_responses(self, responses: list[str | None]) -> None:
        """Configure the sequence of responses for wait_for() calls."""
        self.wait_for_responses = responses
        self._wait_for_call_index = 0


# =============================================================================
# restart() tests
# =============================================================================


@pytest.mark.unit
def test_restart_calls_stop_then_start():
    """restart() should call stop() first, then start()."""
    io = StubIO()
    io.restart()
    assert io.call_history == ["stop", "start"]


# =============================================================================
# wait_for_prompt() tests
# =============================================================================


@pytest.mark.unit
def test_wait_for_prompt_returns_true_when_no_prompt_configured():
    """When prompt is empty, wait_for_prompt() should return True immediately."""
    io = StubIO(prompt="")
    result = io.wait_for_prompt()
    assert result is True
    assert io.call_history == []  # No wait_for calls made


@pytest.mark.unit
def test_wait_for_prompt_returns_true_when_prompt_found_immediately():
    """When prompt is found on first try, return True."""
    io = StubIO(prompt=">>> ")
    io.set_wait_for_responses([">>> "])
    result = io.wait_for_prompt()
    assert result is True


@pytest.mark.unit
def test_wait_for_prompt_sends_newline_and_retries_on_first_failure():
    """When prompt not found initially, send newline and retry."""
    io = StubIO(prompt=">>> ", newline="\n")
    io.set_wait_for_responses([None, ">>> "])  # First fails, second succeeds
    result = io.wait_for_prompt()
    assert result is True
    assert "\n" in io.commands_sent


@pytest.mark.unit
def test_wait_for_prompt_returns_false_when_prompt_never_found():
    """When prompt is never found, return False."""
    io = StubIO(prompt=">>> ", newline="\n")
    io.set_wait_for_responses([None, None])  # Both attempts fail
    result = io.wait_for_prompt()
    assert result is False


# =============================================================================
# run_command() tests
# =============================================================================


@pytest.mark.unit
def test_run_command_sends_command_after_prompt():
    """run_command() should wait for prompt then send the command."""
    io = StubIO(prompt=">>> ")
    io.set_wait_for_responses([">>> ", "expected output"])
    result = io.run_command("ls", expect="expected output")
    assert result == "expected output"
    assert "ls" in io.commands_sent


@pytest.mark.unit
def test_run_command_raises_when_prompt_not_found():
    """run_command() should raise RuntimeError if prompt doesn't appear."""
    io = StubIO(prompt=">>> ", newline="\n")
    io.set_wait_for_responses([None, None])  # Prompt never appears
    with pytest.raises(RuntimeError, match="Prompt does not appear"):
        io.run_command("ls")


@pytest.mark.unit
def test_run_command_retries_on_failure():
    """run_command() should retry up to 'attempts' times."""
    io = StubIO(prompt="")  # No prompt to simplify test
    io.set_wait_for_responses([None, None, "success"])
    result = io.run_command("cmd", expect="success", attempts=3)
    assert result == "success"
    assert io.commands_sent.count("cmd") == 3


@pytest.mark.unit
def test_run_command_returns_none_after_all_attempts_fail():
    """run_command() returns None if all attempts fail."""
    io = StubIO(prompt="")
    io.set_wait_for_responses([None, None])
    result = io.run_command("cmd", expect="success", attempts=2)
    assert result is None


# =============================================================================
# wait_and_consume_logs() tests
# =============================================================================


@pytest.mark.unit
def test_wait_and_consume_logs_calls_wait_for_with_wildcard():
    """wait_and_consume_logs() should call wait_for with '.*' pattern."""
    io = StubIO()
    io.wait_and_consume_logs(timeout_sec=1.0)
    assert "wait_for:.*" in io.call_history
