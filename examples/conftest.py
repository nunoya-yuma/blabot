import pytest

from cli.blabot.blabot.process_io import ProcessIO
from cli.example_cli import ExampleCli


@pytest.fixture(scope="session")
def example_cli():
    start_command = "python3 example.py"
    io_interact = ProcessIO(start_command, "> ")
    example_cli = ExampleCli(io_interact)
    example_cli.start()
    yield example_cli
    example_cli.stop()
