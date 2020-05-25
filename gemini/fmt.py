"""Utilities for formatting strings."""


def human_format_bytes(num: int) -> str:
    """Format an integer number of bytes as a human readable string.

    Args:
        bytes_ (int): integer value of bytes to be formatted.

    Returns:
        str: Human readable string representing the number of bytes input.
    """
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]:
        if abs(num) < float(1024):
            return f"{num:3.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} YiB"
