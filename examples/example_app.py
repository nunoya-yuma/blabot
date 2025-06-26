import logging
import sys
import time
from pathlib import Path

EXAMPLE_PROMPT = "> "
EXAMPLE_FILE_PATH = Path(__file__)
EXAMPLE_START_COMMAND = f"python3 {EXAMPLE_FILE_PATH}"

logger = logging.getLogger(__name__)


class SampleCli:
    def __init__(self):
        self._status = "invalid"
        self._status_list = (
            "invalid",
            "on",
            "off",
        )

    def handle_input(self, input):
        if input == "sample-status":
            self._show_status()
        elif input == "sample-ctrl on":
            self._control_status("on")
        elif input == "sample-ctrl off":
            self._control_status("off")
        else:
            sys.stderr.write(f"Invalid command: {input}\n")
            sys.stderr.flush()

    def _show_status(self):
        logger.info("Sample status: %s", self._status)

    def _control_status(self, command):
        if command not in self._status_list:
            sys.stderr.write("Invalid status command\n")
            sys.stderr.flush()
            return

        if command == self._status:
            logger.info("Sample status does not change: '%s'", self._status)
        else:
            self._status = command
            logger.info("Sample status changed to '%s'", self._status)


if __name__ == "__main__":
    # Configure logger for CLI application
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    example_process = SampleCli()

    # Imitate program startup
    logger.info("Initializing...")
    time.sleep(1)
    logger.info("Complete startup sequence")

    while True:
        cmd = input(EXAMPLE_PROMPT)
        example_process.handle_input(cmd)
