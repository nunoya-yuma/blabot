import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "test_iterations",
    [
        pytest.param(1, marks=pytest.mark.easy),
        pytest.param(5, marks=pytest.mark.hard),
    ],
)
@pytest.mark.simple_process_test
def test_control_command(example_cli, test_iterations):
    for run_count in range(test_iterations):
        logger.info("")
        logger.info("=========================")
        logger.info("Test Run: %d/%d", run_count + 1, test_iterations)
        logger.info("=========================")
        logger.info("")

        assert example_cli.send_on_off("on")
        assert example_cli.wait_for("changed to 'on'")

        assert example_cli.send_on_off("on")
        assert example_cli.wait_for("does not change: 'on'")

        assert example_cli.send_on_off("on")
        assert example_cli.wait_for("does not change: 'on'")

        assert example_cli.send_on_off("off")
        assert example_cli.wait_for("changed to 'off'")

        assert example_cli.send_on_off("off")
        assert example_cli.wait_for("does not change: 'off'")

        assert example_cli.send_on_off("off")
        assert example_cli.wait_for("does not change: 'off'")
