#!/usr/bin/env python3
import sys
import time
from pathlib import Path

EXAMPLE_PROMPT = "> "
EXAMPLE_FILE_PATH = Path(__file__)
EXAMPLE_START_COMMAND = f"python3 {EXAMPLE_FILE_PATH}"


class SampleCli():
    def __init__(self):
        self.status = "invalid"
        self.status_list = (
            "invalid",
            "on",
            "off",
        )

    def HandleInput(self, input):
        if input == "sample-status":
            self._ShowStatus()
        elif input == "sample-ctrl on":
            self._ControlStatus("on")
        elif input == "sample-ctrl off":
            self._ControlStatus("off")
        else:
            sys.stderr.write(f"Invalid command: {input}\n")
            sys.stderr.flush()

    def _ShowStatus(self):
        print(f"Sample status: {self.status}")

    def _ControlStatus(self, command):
        if command not in self.status_list:
            sys.stderr.write("Invalid status command\n")
            sys.stderr.flush()
            return

        if command == self.status:
            print(f"Sample status does not change: '{self.status}'")
        else:
            self.status = command
            print(f"Sample status changed to '{self.status}'")


if __name__ == "__main__":
    example_process = SampleCli()

    # Imitate program startup
    print("Initializing...")
    time.sleep(1)
    print("Complete startup sequence")

    while True:
        cmd = input(EXAMPLE_PROMPT)
        example_process.HandleInput(cmd)
