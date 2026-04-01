from __future__ import annotations

import re

import aoc

_AT_LEAST_THREE_VOWELS = re.compile(r"^(.*[aeiou]){3}.*$")
_LETTER_TWICE_IN_A_ROW = re.compile(r"^.*(.)\1.*$")
_DISALLOWED_SUBSTRINGS = re.compile(r"^.*(ab|cd|pq|xy).*$")


def is_nice_string(string) -> bool:
    return (
        bool(_AT_LEAST_THREE_VOWELS.search(string))
        and bool(_LETTER_TWICE_IN_A_ROW.search(string))
        and not bool(_DISALLOWED_SUBSTRINGS.search(string))
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
        "ugknbfddgicrmopn",
        "aaa",
        "xxoplsenni",
    ],
)
def test_is_nice_string(string):
    assert is_nice_string(string)


@pytest.mark.parametrize(
    "string",
    [
        "jchzalrnumimnmhp",
        "haegwjzuvuyypxyu",
        "dvszwmarrgswjxmb",
        "a",
        "xx",
        "aaeiab",
    ],
)
def test_is_naughty_string(string):
    assert not is_nice_string(string)


@pytest.mark.parametrize(
    "lines,result",
    [
        (
            "ugknbfddgicrmopn\n"
            "aaa\n"
            "jchzalrnumimnmhp\n"
            "haegwjzuvuyypxyu\n"
            "dvszwmarrgswjxmb\n",
            2,
        ),
        ("\n", 0),
        ("aaei\n", 1),
        ("abeei\n", 0),
    ],
)
def test_count_nice_strings(lines, result):
    assert result == count_nice_strings(lines)
