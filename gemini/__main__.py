"""gemini is a command line tool for finding duplicate files within a
directory."""
import hashlib
from collections import defaultdict
from pathlib import Path
from pprint import pprint

import click
from loguru import logger

from gemini import __version__
from gemini.fmt import human_format_bytes

BLOCK_SIZE = 1024 * 1024


def hash_file(file: Path, hash_algorithm="sha1") -> str:
    """Hashes a file and returns the hexdigest.

    Args:
        file (Path): Path to the file to hash
        hash_algorithm (str, optional): hashlib hash algorithm to use.
            Defaults to "sha1".

    Returns:
        str: hexdigest of the file.
    """
    logger.info("Working on: {0}".format(file))

    hasher = hashlib.new(hash_algorithm)
    with open(file, "rb") as file_to_hash:
        buf = file_to_hash.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file_to_hash.read(BLOCK_SIZE)

    digest = hasher.hexdigest()
    logger.info(digest)
    return digest


@logger.catch
@click.command()
@click.version_option(version=__version__)
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
def find_duplicates(directory):
    """Determines if any files within the input directory are duplicates of
    one-another.
    """
    dir_path = Path(directory)

    duplicates = defaultdict(list)
    same_size = defaultdict(list)
    files = (i for i in dir_path.rglob("*") if i.is_file())

    # Optimize looking for duplicates only among files that have the same size.
    for f in files:
        same_size[f.stat().st_size].append(f)

    # Groups file paths by content hash, paths containing identical content
    # will be grouped together.
    path_set = (l for l in same_size.values() if len(l) > 1)
    for paths in path_set:
        for file_path in paths:
            duplicates[hash_file(file_path)].append(file_path)

    print(80 * "#")
    real_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
    pprint(real_duplicates)
    print(80 * "#")

    for v in real_duplicates.values():
        size_on_disk = v[0].stat().st_size * len(v)
        dedupable = 1.0 / len(v)
        print(
            f"Size On Disk: {human_format_bytes(size_on_disk)}, Dedupable: {dedupable:.0%}"
        )


def main():
    """Main entrypoint for the CLI.
    """
    find_duplicates()  # pylint: disable=no-value-for-parameter
