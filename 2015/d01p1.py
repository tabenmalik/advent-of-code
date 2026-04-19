from __future__ import annotations

from collections import Counter
from collections import Counter as TypingCounter

import aoc


def ending_floor(directions: str) -> int:
    counts: TypingCounter[str] = Counter(directions)
    return counts["("] - counts[")"]


if __name__ == "__main__":
    raise SystemExit(aoc.problem_entry_point(ending_floor, 2015, 1))


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "directions,floor",
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
        (aoc.get_input(2015, 1), 280),
    ],
)
def test_solve(directions, floor):
    assert ending_floor(directions) == floor
