#!/bin/python3
import sys

if __name__ == "__main__":
    prompt = "> "
    while True:
        cmd = input(prompt)
        print(f"[INFO] {cmd}", end="")
        sys.stderr.write(f"[ERROR] {cmd}\n")
        sys.stderr.flush()
        print(f"[INFO] {cmd} 2nd")
        sys.stdout.flush()
