#!/bin/python3

import io_interact
import pexpect
import sys


class ProgramIO(io_interact.IOInteractBase):
    def __init__(self, start_command: str):
        super().__init__()
        self.prompt: str = "> "
        self.newline: str = "\n"
        self.start_command = start_command

    def start(self):
        if self.process:
            raise RuntimeError("Process has already started")

        self.process = pexpect.spawn(self.start_command)
        self.process.logfile = sys.stdout.buffer

    def stop(self):
        if not self.process:
            raise RuntimeError("Process not started")

        self.process.terminate()
        # self.process.kill()
        self.process.wait()
        self.process = None

    def send_command(self, command) -> None:
        self.process.sendline(command)

    def wait_for(self, expect, timeout_sec: float = 3.0) -> str:
        if not self.process:
            raise RuntimeError("Process not started")

        expect_list = [
            pexpect.EOF,
            pexpect.TIMEOUT,
        ]
        expect_list.append(expect)
        index = self.process.expect(expect_list, timeout=timeout_sec)

        match = None
        if index == 0:
            # pexpect.EOF is output
            # TODO: Consider handling in this case
            pass
        elif index == 1:
            # pexpect.TIMEOUT is output
            # This means that no matching string was output until the timeout.
            pass
        else:
            match = self.process.after.decode("utf-8")

        return match


if __name__ == "__main__":
    inst = ProgramIO("./sample.py")
    inst.start()
    ret = inst.run_command("test", "aaa")
    print(f"\n\nresult: {ret}")

    print("Restart!")
    inst.restart()
    ret = inst.run_command("test", "2nd")
    print(f"\n\nresult: {ret}")

    ret = inst.run_command("test")
    print(f"\n\nresult: {ret}")
    inst.stop()
