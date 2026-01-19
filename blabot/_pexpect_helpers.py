"""Helper functions for pexpect-based process communication."""

import pexpect
from pexpect_serial import SerialSpawn


def wait_for_pattern(
    process: pexpect.spawn | SerialSpawn,
    expect: str,
    timeout_sec: float = 3.0,
) -> str | None:
    """Wait for expected pattern in process output.

    Args:
        process: pexpect-compatible process object.
        expect: Regular expression pattern to wait for.
        timeout_sec: Maximum time to wait in seconds.

    Returns:
        str: The matched string if pattern is found.
        None: If timeout occurs before pattern is matched.

    Raises:
        TypeError: If the matched output is not bytes.

    """
    try:
        process.expect(expect, timeout=timeout_sec)
    except pexpect.TIMEOUT:
        return None

    if not isinstance(process.after, bytes):
        err_msg = "Expected bytes from process.after"
        raise TypeError(err_msg)

    return process.after.decode("utf-8")
