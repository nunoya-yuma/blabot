#!/bin/bash

set -e

socat PTY,link=/tmp/ttyV0,echo=0 PTY,link=/tmp/ttyV1,echo=0 &
sleep 1
cd $(dirname $0)/..
uv run python example_app.py </tmp/ttyV0 >/tmp/ttyV0 2>&1 &
uv run pytest -v -s -m "device_test" tests/

exit 0
