from __future__ import annotations

import re

import aoc

RE_MEM_CHARS = re.compile(r'(\\\\|\\"|\\x[a-f0-9]{2}|[^"])')


def char_diff(santa_list: str) -> int:
    code_chars = 0
    mem_chars = 0
    for line in santa_list.strip().splitlines():
        code_chars += len(line)
        unquoted_line = line[1:-1]
        code_points = RE_MEM_CHARS.findall(unquoted_line)
        mem_chars += len(code_points)

    diff = code_chars - mem_chars
    return diff


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(char_diff, 2015, 8),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "santa_list,result",
    [
        ('""', 2),
        ('"abc"', 2),
        (r'"aaa\"aaa"', 3),
        (r'"\x27"', 5),
        (r'""\n"abc"\n"aaa\"aaa"\n"\x27"', 12),
        (r'"ab\x34\"five\\"', 7),
        (r'"\x2bv"', 5),
        (r'"\"', 2),
        (r'"abc\"', 2),
        (r'"\xff\xzz"', 5),
        (aoc.get_input(2015, 8), 1342),
    ],
)
def test_char_diff(santa_list, result):
    assert result == char_diff(santa_list)
