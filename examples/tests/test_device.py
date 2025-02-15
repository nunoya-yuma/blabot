"""
This file is a test for input/output and exchange of device type files.
Before running this test, follow the README
and prepare the process for testing.

The following is an example command.
Prepare virtual device
$ socat PTY,link=/tmp/ttyV0 PTY,link=/tmp/ttyV1 &

Run example_app.py with input/output set to /tmp/ttyV0
$ cd ${BLABOT}/examples/
$ ./example_app.py < /tmp/ttyV0 > /tmp/ttyV0 2>&1
"""
from blabot.device_io import DeviceIO
import pytest

from ..example_cli import ExampleCli
from ..example_app import EXAMPLE_PROMPT


@pytest.fixture
def device_io_cli():
    DEVICE_PORT = "/tmp/ttyV1"
    io_interact = DeviceIO(DEVICE_PORT, prompt=EXAMPLE_PROMPT)

    device_io_cli = ExampleCli(io_interact)
    device_io_cli.start()
    yield device_io_cli
    device_io_cli.stop()


@pytest.mark.device_test
def test_device(device_io_cli):
    # At the very beginning, the following logs will appear
    # and should be ignored.
    # > Invalid command:

    # The first state should be OFF for sure.
    assert device_io_cli.send_on_off("off")

    assert device_io_cli.send_on_off("on")
    assert device_io_cli.wait_for("changed to 'on'")

    assert device_io_cli.send_on_off("on")
    assert device_io_cli.wait_for("does not change: 'on'")

    assert device_io_cli.send_on_off("on")
    assert device_io_cli.wait_for("does not change: 'on'")

    assert device_io_cli.send_on_off("off")
    assert device_io_cli.wait_for("changed to 'off'")

    assert device_io_cli.send_on_off("off")
    assert device_io_cli.wait_for("does not change: 'off'")

    assert device_io_cli.send_on_off("off")
    assert device_io_cli.wait_for("does not change: 'off'")
