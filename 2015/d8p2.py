from __future__ import annotations

import re

import aoc


def encode(line: str) -> str:
    return f'"{re.sub(r'("|\\)', r'\\\1', line)}"'


def char_diff(santa_list: str) -> str:
    code_chars = 0
    encoded_code_chars = 0
    for line in santa_list.strip().splitlines():
        code_chars += len(line)
        encoded_code_chars += len(encode(line))

    return str(encoded_code_chars - code_chars)


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(char_diff, 2015, 8),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "line,encoded",
    [
        ('""', r'"\"\""'),
        ('"abc"', r'"\"abc\""'),
        (r'"aaa\"aaa"', r'"\"aaa\\\"aaa\""'),
        (r'"\x27"', r'"\"\\x27\""'),
    ],
)
def test_encode(line, encoded):
    assert encoded == encode(line)


@pytest.mark.parametrize(
    "santa_list,result",
    [
        ('""', "4"),
        (r'"abc"', "4"),
        (r'"aaa\"aaa"', "6"),
        (r'"\x27"', "5"),
    ],
)
def test_char_diff(santa_list, result):
    assert result == char_diff(santa_list)
