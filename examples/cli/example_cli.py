import re

from .nn_io_interact.nn_io_interact.templated_io import TemplatedIO


class ExampleCliBase():
    def __init__(self, io_interact: TemplatedIO):
        self.io_interact = io_interact

    def __getattr__(self, name):
        """
        Call TemplateIO class method

        This enables to call TemplatedIO class method
        e.g.) self.run_command(...)
        You don't have to call self.io_interact.run_command(...)
        """
        return getattr(self.io_interact, name)

    def status_show(self):
        pattern = "Sample status: (invalid|on|off)"

        output = self.run_command("sample-status", pattern)
        if output is None:
            return None

        match = re.search(pattern, output)
        res = match.group(1) if match else None
        return res

    def send_on_off(self, command: str):
        pattern = "Sample status"
        return self.run_command(f"sample-ctrl {command}", pattern)


class ExampleCli(ExampleCliBase):
    def check_startup(self):
        assert self.wait_for("Initializing...")

        assert self.wait_for("Complete startup sequence")

        status = self.status_show()
        assert status == "invalid", f"status is {status}"
