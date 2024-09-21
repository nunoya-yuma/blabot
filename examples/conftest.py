import pytest
import re

from nn_io_interact.nn_io_interact.process_io import ProcessIO


class ExampleCli(ProcessIO):
    def __init__(self, start_command: str, prompt="> "):
        super().__init__(start_command, prompt)

    def status_show(self):
        pattern = "Sample status: (invalid|on|off)"

        output = self.run_command("sample-status", pattern)
        if output is None:
            return None

        match = re.search(pattern, output)
        res = match.group(1) if match else None
        return res

    def SendOnOff(self, command: str):
        pattern = "Sample status"
        return self.run_command(f"sample-ctrl {command}", pattern)


@pytest.fixture(scope="session")
def example_cli():
    start_command = "python3 example.py"
    example_cli = ExampleCli(start_command)
    yield example_cli
    example_cli.stop()
