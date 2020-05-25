from pathlib import Path

from gemini.__main__ import hash_file


def test_my_fakefs(fs):
    p = Path("file.txt")
    fs.create_file(p, contents="content")
    assert hash_file(p) == "040f06fd774092478d450774f5ba30c5da78acc8"
