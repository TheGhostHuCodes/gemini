import pytest

from gemini.fmt import human_format_bytes


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (42, "42.00 B"),
        (1024, "1.00 KiB"),
        (1048576, "1.00 MiB"),
        (1073741824, "1.00 GiB"),
        (1099511627776, "1.00 TiB"),
        (1125899906842624, "1.00 PiB"),
        (1152921504606846976, "1.00 EiB"),
        (1180591620717411303424, "1.00 ZiB"),
        (1208925819614629174706176, "1.00 YiB"),
    ],
)
def test_human_format_bytes_returns_expected_string(test_input, expected):
    assert human_format_bytes(test_input) == expected
