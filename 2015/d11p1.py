from __future__ import annotations

import re
import string
from collections import deque
from itertools import islice

import aoc


# recipe provided by python docs
def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 3) → ABC BCD CDE DEF EFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


RE_INVALID_CHARS = re.compile("[iol]")

RE_PAIRS = re.compile(r"(([a-z])\2)")

RE_STRAIGHT = re.compile(
    "(" + "|".join(map("".join, sliding_window(string.ascii_lowercase, 3))) + ")"
)


def increment_password(password: str) -> str:
    if not password:
        return ""
    if password[-1] == "z":
        return increment_password(password[:-1]) + "a"
    return password[:-1] + chr(ord(password[-1]) + 1)


def is_valid(password: str) -> bool:
    pair_match = RE_PAIRS.findall(password)
    return (
        not bool(RE_INVALID_CHARS.search(password))
        and (bool(pair_match) and len(set(pair_match)) >= 2)
        and bool(RE_STRAIGHT.search(password))
    )


def next_valid_password(prev_password: str) -> str:
    prev_password = prev_password.strip()
    password = increment_password(prev_password)
    while not is_valid(password):
        password = increment_password(password)
    return password


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(next_valid_password, 2015, 11),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "prev,next_",
    [
        ("a", "b"),
        ("b", "c"),
        ("z", "a"),
        ("aa", "ab"),
        ("az", "ba"),
        ("zy", "zz"),
        ("zz", "aa"),
    ],
)
def test_increment_password(prev, next_):
    assert next_ == increment_password(prev)


@pytest.mark.parametrize(
    "password",
    [
        "hijklmmn",
        "abbceffg",
        "abbcegjk",
    ],
)
def test_invalid_passwords(password):
    assert not is_valid(password)


@pytest.mark.parametrize(
    "password",
    [
        "abcdffaa",
        "ghjaabcc",
        "aabbccabc",
    ],
)
def test_valid_passwords(password):
    assert is_valid(password)


@pytest.mark.parametrize(
    "prev_password,password",
    [
        ("abcdefgh", "abcdffaa"),
        ("ghijklmn", "ghjaabcc"),
        (aoc.get_input(2015, 11), "vzbxxyzz"),
    ],
)
def test_next_valid_password(prev_password, password):
    assert password == next_valid_password(prev_password)
