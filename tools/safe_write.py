"""Writes that can't leave the profile half-changed.

The refresh scripts each rewrite README.md and tools/counts.json, often more than once (a
chart's alt text is written from the counts just stored). Two things could leave those
files wrong:

- a run that stops part way (a README sentence a later step can't find, a network error,
  Ctrl+C) after the first write: all_or_nothing() puts every file back as it was;
- a write cut off mid-file (a crash, a kill, OneDrive holding the file): write() puts the
  text in a temporary file beside the target and renames it over, so the target is
  either the old text or the new, never part of one.

    with all_or_nothing(README, COUNTS):
        write(COUNTS, ...)
        write(README, ...)
"""
import contextlib
import os
import time
from pathlib import Path


def _replace(tmp, path):
    # OneDrive can hold a lock on a file it's syncing for a moment; wait it out briefly.
    for attempt in range(10):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 9:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(0.5)


def write_bytes(path, data):
    path = Path(path)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(data)
    _replace(tmp, path)


def write(path, text):
    """Write text to path as UTF-8 with LF line ends, all at once."""
    write_bytes(path, text.replace("\r\n", "\n").encode("utf-8"))


@contextlib.contextmanager
def all_or_nothing(*paths):
    """If the block stops for any reason, sys.exit and Ctrl+C included, put each path back
    as it was before the block (removing any the block created)."""
    paths = [Path(p) for p in paths]
    before = {p: p.read_bytes() if p.exists() else None for p in paths}
    try:
        yield
    except BaseException:
        for p, data in before.items():
            if data is None:
                p.unlink(missing_ok=True)
            elif not p.exists() or p.read_bytes() != data:
                write_bytes(p, data)
        raise
