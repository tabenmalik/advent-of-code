from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import NamedTuple
from unittest.mock import MagicMock

import pytest

import aoc


class Fixture(NamedTuple):
    cache: Path
    data: Path
    cookie_file: Path
    urlopen_mock: MagicMock


@pytest.fixture
def getup(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    cache.mkdir()
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache))
    cache = cache / "aoc"
    cache.mkdir()

    data = tmp_path / "data"
    data.mkdir()
    monkeypatch.setenv("XDG_DATA_HOME", str(data))
    data = data / "aoc"
    data.mkdir()

    cookie_file = data / "session_cookie.txt"
    cookie_file.write_text("session=1234abcd\n")

    urlopen_mock = MagicMock()
    urlopen_mock.return_value.status = 200
    monkeypatch.setattr(aoc.request, "urlopen", urlopen_mock)

    return Fixture(cache, data, cookie_file, urlopen_mock)


def test_get_input_in_cache(getup):
    cached_input = getup.cache / "2025-01.txt"
    cached_input.write_text("hello\nworld\n!!\n")
    problem_input = aoc.get_input(2025, 1)
    assert problem_input == "hello\nworld\n!!\n"


def test_get_input_successful_request(getup):
    getup.urlopen_mock.return_value.read().decode.return_value = (
        "this is downloaded input\n" "another line of input\n"
    )

    problem_input = aoc.get_input(2026, 20)
    expected_cache_file = getup.cache / "2026-20.txt"
    assert expected_cache_file.exists()
    assert expected_cache_file.stat().st_mode & 0o777 == 0o600
    assert expected_cache_file.read_text() == (
        "this is downloaded input\n" "another line of input\n"
    )
    assert problem_input == ("this is downloaded input\n" "another line of input\n")


def test_successful_problem_entry_point(getup):
    cached_input = getup.cache / "2049-02.txt"
    cached_input.write_text("hello\n")
    solver_function = MagicMock()
    assert 0 == aoc.problem_entry_point(solver_function, 2049, 2, tuple())
    assert solver_function.called


def test_start_problem(capsys, tmp_path):
    assert 0 == aoc.start_problem(("2025", "2"))
    captured = capsys.readouterr()
    assert re.search(r"problem_entry_point\(solve, 2025, 2\)", captured.out)

    # don't care about the exact output of start_problem
    # but it needs to pass all of my linting checks
    tmp_file = tmp_path / "start.py"
    tmp_file.write_text(captured.out)
    cp = subprocess.run(["pre-commit", "run", "--files", str(tmp_file)])
    assert cp.returncode == 0
