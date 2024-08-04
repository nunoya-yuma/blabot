#!/bin/python3

import io_interact
import pexpect


class ProgramIO(io_interact.IOInteractBase):
    def __init__(self, spawn_command: str):
        super().__init__()
        self.start_command = spawn_command

    def start(self):
        if self.process:
            raise RuntimeError("Process has already started")

        self.process = pexpect.spawn(self.start_command)

    def stop(self):
        if not self.process:
            raise RuntimeError("Process not started")

        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.terminate()
        # self.process.kill()
        self.process.wait()

    def send_command(self, command) -> None:
        self.process.sendline(command)

    def wait_for(self, expect, timeout_sec: float = 3.0) -> str:
        if not self.process:
            raise RuntimeError("Process not started")

        index = self.process.expect(expect, timeout=timeout_sec)

        match = None
        print(self.process.before.decode("utf-8"), end="")
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
            print(match, end="")

        return match

    def run_command(
            self,
            cmd: str = "",
            expect: str = "",
            timeout_sec: float = 0.2,
            attempts: int = 1) -> str:

        if not self.process:
            raise RuntimeError("Process not started")

        expect_list = [
            pexpect.EOF,
            pexpect.TIMEOUT,
        ]
        expect_list.append(expect)

        self.send_command(cmd)
        match = self.wait_for(expect_list, timeout_sec=timeout_sec)

        return match


if __name__ == "__main__":
    inst = ProgramIO("./sample.py")
    inst.start()
    ret = inst.run_command("test", "aaa")
    print(f"\n\nresult: {ret}")
    ret = inst.run_command("test", "2nd")
    print(f"\n\nresult: {ret}")
    ret = inst.run_command("test")
    print(f"\n\nresult: {ret}")
