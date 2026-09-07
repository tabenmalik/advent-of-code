from __future__ import annotations

import aoc


def cantor_pair(a: int, b: int) -> int:
    return ((a + b) * (a + b + 1)) // 2 + b


def code(a: int, b: int) -> int:
    index = cantor_pair(a - 1, b - 1) + 1

    value = 20151125
    for _ in range(2, index + 1):
        value = (value * 252533) % 33554393

    return value


def solve(inp: str) -> int:
    words = inp.strip().split()
    a = int(words[15].strip(","))
    b = int(words[17].strip("."))
    return code(a, b)


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 25),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "a,b,p",
    [
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, 2),
        (5, 0, 15),
    ],
)
def test_cantor_pair(a: int, b: int, p: int) -> None:
    assert cantor_pair(a, b) == p


@pytest.mark.parametrize(
    "a, b, c",
    [
        (1, 1, 20151125),
        (2, 1, 31916031),
        (1, 2, 18749137),
        (6, 1, 33071741),
        (1, 6, 33511524),
    ],
)
def test_code(a: int, b: int, c: int) -> None:
    assert code(a, b) == c


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 25), 2650453)])
def test_solve(inp: str, result: int) -> None:
    assert result == solve(inp)
