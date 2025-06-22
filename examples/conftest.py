import pytest

from blabot.process_io import ProcessIO

from .example_app import EXAMPLE_PROMPT, EXAMPLE_START_COMMAND
from .example_cli import ExampleCli


@pytest.fixture(scope="session")
def example_cli():
    io_interact = ProcessIO(EXAMPLE_START_COMMAND, EXAMPLE_PROMPT)
    example_cli = ExampleCli(io_interact)
    example_cli.start()
    yield example_cli
    example_cli.stop()
