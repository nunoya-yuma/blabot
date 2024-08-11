from nn_io_interact import program_io
import re


class process_cli(program_io.ProgramIO):
    def __init__(self, start_command: str):
        super().__init__(start_command)

    def status_show(self):
        pattern = "Sample status: (invalid|on|off)"

        output = self.run_command("sample-status", pattern)
        if output is None:
            return None

        match = re.search(pattern, output)
        res = match.group(1) if match else None
        return res


def test_startup():
    start_command = "python3 example.py"
    example_cli = process_cli(start_command)
    example_cli.start()

    assert example_cli.wait_for("Initializing...")

    assert example_cli.wait_for("Complete startup sequence")

    status = example_cli.status_show()
    assert status == "invalid", f"status is {status}"
