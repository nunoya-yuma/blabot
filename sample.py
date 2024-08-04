#!/bin/python3
import sys
import time

if __name__ == "__main__":
    prompt = "> "
    time.sleep(2)
    while True:
        cmd = input(prompt)

        if cmd == "":
            continue

        print(f"[INFO] {cmd}", end="")
        sys.stderr.write(f"[ERROR] {cmd}\n")
        sys.stderr.flush()
        print(f"[INFO] {cmd} 2nd")
        sys.stdout.flush()
