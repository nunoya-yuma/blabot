import pytest


@pytest.mark.easy
@pytest.mark.hard
@pytest.mark.order("first")
def test_startup(example_cli):
    example_cli.start()

    assert example_cli.wait_for("Initializing...")

    assert example_cli.wait_for("Complete startup sequence")

    status = example_cli.status_show()
    assert status == "invalid", f"status is {status}"
