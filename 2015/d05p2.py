from __future__ import annotations

import re

import aoc

_PAIR_OF_TWO_LETTERS = re.compile(r"^.*([a-zA-Z]{2}).*\1.*$")
_LETTER_SANDWHICH = re.compile(r"^.*([a-zA-Z])[a-zA-Z]\1.*$")


def is_nice_string(string) -> bool:
    return bool(_PAIR_OF_TWO_LETTERS.search(string)) and bool(
        _LETTER_SANDWHICH.search(string)
    )


def count_nice_strings(lines: str) -> int:
    nice_strings = filter(is_nice_string, lines.strip().splitlines())
    return len(tuple(nice_strings))


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(count_nice_strings, 2015, 5),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "string",
    [
        "qjhvhtzxzqqjkmpb",
        "xxyxx",
    ],
)
def test_is_nice_string(string):
    assert is_nice_string(string)


@pytest.mark.parametrize(
    "string",
    [
        "aaa",
        "xyx",
        "aabcdefgaa",
        "abcdefeghi",
        "uurcxstgmygtbstg",
        "ieodomkazucvgmuy",
    ],
)
def test_is_naughty_string(string):
    assert not is_nice_string(string)


@pytest.mark.parametrize(
    "lines,result",
    [
        ("\n", 0),
        ("xxyxx\nqjhvhtzxzqqjkmpb\n", 2),
        ("uurcxstgmygtbstg\nieodomkazucvgmuy\n", 0),
        ("uurcxstgmygtbstg\nxxyxx\nqjhvhtzxzqqjkmpb\nieodomkazucvgmuy\n", 2),
        (aoc.get_input(2015, 5), 53),
    ],
)
def test_count_nice_strings(lines, result):
    assert result == count_nice_strings(lines)
