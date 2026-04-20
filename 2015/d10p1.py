from __future__ import annotations

from itertools import groupby

import aoc

# choosing to operate on strings rather than numbers since
# a.) the operations to use a best suited for strings
# b.) avoiding overhead of conversions back and forth
# c.) avoiding python's integer string conversion length limitation.
#     it can be overriden by why deal with that


def look_and_say(n: str) -> str:
    result = ""
    for char, group in groupby(n):
        result += f"{len(tuple(group))}{char}"
    return result


def length_of_final_look_and_say(start: str, iterations: int = 40) -> int:
    n = start.strip()
    for _ in range(iterations):
        n = look_and_say(n)
    return len(n)


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(length_of_final_look_and_say, 2015, 10),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "n,result",
    [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
    ],
)
def test_look_and_say(n, result):
    assert result == look_and_say(n)


@pytest.mark.parametrize(
    "start,iterations,length",
    [
        ("1", 0, 1),
        ("1", 1, 2),
        ("1", 2, 2),
        ("1", 3, 4),
        ("1", 4, 6),
        ("1", 5, 6),
        ("1211", 2, 6),
        (aoc.get_input(2015, 10), 40, 492982),
    ],
)
def test_length_of_final_look_and_say(start, iterations, length):
    assert length == length_of_final_look_and_say(start, iterations)
