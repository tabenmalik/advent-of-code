from __future__ import annotations

from collections.abc import Iterator
from itertools import count
from math import isqrt

import aoc


def divisors(n: int) -> Iterator[int]:
    """Return all divisors of `n` in no particular order."""
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            yield i
            j = n // i
            if j != i:
                yield j


def presents(house: int) -> int:
    return sum(divisors(house)) * 10


def solve(inp: str) -> int:
    target_presents = int(inp)

    for house in count(1):
        if presents(house) >= target_presents:
            return house

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 20),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "inp,result",
    [
        ("10\n", 1),
        ("20\n", 2),
        ("80\n", 6),
        ("150\n", 8),
        (aoc.get_input(2015, 20), 776160),
    ],
)
def test_solve(inp, result):
    assert result == solve(inp)
