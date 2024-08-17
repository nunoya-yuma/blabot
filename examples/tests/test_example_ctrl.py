import pytest
import sys


@pytest.mark.parametrize(
    ("attempts"), [
        pytest.param(1, marks=pytest.mark.easy),
        pytest.param(5, marks=pytest.mark.hard),
    ]
)
def test_control_command(example_cli, attempts):
    print(attempts)
    for attempt in range(attempts):
        print("")
        print("=========================")
        print(f"Attempt: {attempt+1}/{attempts}")
        print("=========================")
        print("")
        sys.stdout.flush()

        assert example_cli.SendOnOff("on")
        assert example_cli.wait_for("changed to 'on'")

        assert example_cli.SendOnOff("on")
        assert example_cli.wait_for("does not change: 'on'")

        assert example_cli.SendOnOff("on")
        assert example_cli.wait_for("does not change: 'on'")

        assert example_cli.SendOnOff("off")
        assert example_cli.wait_for("changed to 'off'")

        assert example_cli.SendOnOff("off")
        assert example_cli.wait_for("does not change: 'off'")

        assert example_cli.SendOnOff("off")
        assert example_cli.wait_for("does not change: 'off'")
