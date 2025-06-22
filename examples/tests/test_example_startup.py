import pytest


@pytest.mark.easy
@pytest.mark.hard
@pytest.mark.simple_process_test
@pytest.mark.order("first")
def test_startup(example_cli):
    example_cli.check_startup()


@pytest.mark.easy
@pytest.mark.simple_process_test
def test_consume_logs(example_cli):
    # Output should be the following
    # > aaa
    # Invalid command: aaa
    example_cli.run_command("aaa", "bbb")

    example_cli.wait_and_consume_logs(1)

    assert example_cli.wait_for("Invalid command: ", 1) is None, (
        "Output logs are not consumed"
    )
