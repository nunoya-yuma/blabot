from blabot.process_io import ProcessIO

import pytest

from .example_cli import ExampleCli
from .example import EXAMPLE_START_COMMAND, EXAMPLE_PROMPT


@pytest.fixture(scope="session")
def example_cli():
    io_interact = ProcessIO(EXAMPLE_START_COMMAND, EXAMPLE_PROMPT)
    example_cli = ExampleCli(io_interact)
    example_cli.start()
    yield example_cli
    example_cli.stop()
