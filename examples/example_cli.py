import re

from blabot.templated_io import TemplatedIO


class ExampleCliBase:
    def __init__(self, io_interact: TemplatedIO):
        self._io_interact = io_interact

    def __getattr__(self, name):
        """
        Call TemplateIO class method

        This enables to call TemplatedIO class method
        e.g.) self.run_command(...)
        You don't have to call self.io_interact.run_command(...)
        """
        return getattr(self._io_interact, name)

    def status_show(self):
        PATTERN = "Sample status: (invalid|on|off)"

        output = self.run_command("sample-status", PATTERN)
        if output is None:
            return None

        match = re.search(PATTERN, output)
        return match.group(1) if match else None

    def send_on_off(self, command: str):
        PATTERN = "Sample status"
        return self.run_command(f"sample-ctrl {command}", PATTERN)


class ExampleCli(ExampleCliBase):
    def check_startup(self):
        assert self.wait_for("Initializing...")

        assert self.wait_for("Complete startup sequence")

        status = self.status_show()
        assert status == "invalid", f"status is {status}"
