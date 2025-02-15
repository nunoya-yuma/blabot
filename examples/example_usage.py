#!/usr/bin/env python3

"""
This file provides a sample of how to use the package's features.

This file introduces the usage of `process_io`, one of the classes provided
by this package.
In this sample, example_app.py in the same directory that mimic the software
to be tested are started, and commands are sent and received.
Basically, the usage is the same with respect to other classes.
Hopefully this sample will be useful for those of you who use it
in your own projects.
"""

from blabot.process_io import ProcessIO
from example_app import EXAMPLE_PROMPT, EXAMPLE_START_COMMAND


def main():
    example_cli = ProcessIO(EXAMPLE_START_COMMAND, EXAMPLE_PROMPT)

    example_cli.start()

    assert example_cli.wait_for("Initializing...")
    assert example_cli.wait_for("Complete startup sequence")

    assert example_cli.run_command("sample-status", "Sample status: invalid")

    assert example_cli.run_command(
        "sample-ctrl on", "Sample status changed to 'on'")
    assert example_cli.run_command("sample-status", "Sample status: on")

    assert example_cli.run_command(
        "sample-ctrl off", "Sample status changed to 'off'")
    assert example_cli.run_command("sample-status", "Sample status: off")

    example_cli.stop()


if __name__ == "__main__":
    main()
