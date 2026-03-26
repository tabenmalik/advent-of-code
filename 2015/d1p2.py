from __future__ import annotations

import aoc


def first_time_in_basement(directions: str) -> int:
    floor = 0
    for index, direction in enumerate(directions):
        floor += 1 if direction == "(" else -1
        if floor == -1:
            break
    return index + 1


if __name__ == "__main__":
    raise SystemExit(aoc.problem_entry_point(first_time_in_basement, 2015, 1))


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "directions,index",
    [
        (")", 1),
        ("()())", 5),
        ("()))()(())", 3),
        (aoc.get_input(2015, 1), 1797),
    ],
)
def test_solve(directions, index):
    assert first_time_in_basement(directions) == index
