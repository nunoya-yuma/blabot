
def test_control_command(example_cli):
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
