"""
Supporting functions for Advent of Code development.
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from collections.abc import Sequence
from pathlib import Path
from urllib import request


def xdg_cache_home() -> Path:
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))


def xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def _fetch_input(year: int, day: int) -> str:
    """
    Download input data from website.

    Requires an active session cookie header written to
    `$XDG_DATA_HOME/aoc/session_cookie.txt`.
    """
    cookie_file = xdg_data_home() / "aoc" / "session_cookie.txt"
    session_cookie = cookie_file.read_text().strip()
    headers = {"Cookie": f"{session_cookie}", "User-Agent": "Taben Malik"}
    req = request.Request(
        f"https://www.adventofcode.com/{year}/day/{day}/input", headers=headers
    )
    resp = request.urlopen(req)
    return resp.read().decode()


def get_input(year: int, day: int) -> str:
    """
    Return the input text for a given day.

    Input files are store at `$XDG_CACHE_HOME/aoc/`.
    If an input file does not exist then attempts
    to fetch and cache the input from adventofcode.com
    """
    cache_file = xdg_cache_home() / "aoc" / f"{year}-{day:02d}.txt"
    if not cache_file.exists():
        content = _fetch_input(year, day)
        # use a tmp file to ensure atomic write of end dest
        tmp_cache_file = cache_file.with_suffix(".tmp")
        tmp_cache_file.parent.mkdir(exist_ok=True, parents=True)
        tmp_cache_file.touch()
        tmp_cache_file.chmod(0o600)
        tmp_cache_file.write_text(content)
        tmp_cache_file.replace(cache_file)

    return cache_file.read_text()


def problem_entry_point(
    func: Callable[[str], object],
    year: int,
    day: int,
    argv: Sequence[str] | None = None,
) -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args(argv)

    problem_input = get_input(year, day)
    solution = str(func(problem_input))

    print(solution)
    return 0
