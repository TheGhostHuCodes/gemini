"""Utilities for formatting strings."""


def human_format_bytes(num: int) -> str:
    """Format an integer number of bytes as a human readable string.

    Args:
        num (int): integer value of bytes to be formatted.

    Returns:
        str: Human readable string representing the number of bytes input.
    """
    result = float(num)
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]:
        if abs(result) < float(1024):
            return f"{result:3.2f} {unit}"
        result /= 1024.0
    return f"{result:.2f} YiB"
