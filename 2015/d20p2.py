from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
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
    return sum(d for d in divisors(house) if house / d <= 50) * 11


def solve(inp: str) -> int:
    target_presents = int(inp)

    # see d20p1 for an explaination on why only even
    # numbers need to be checked.
    for house in chain([1, 2, 3], count(4, 2)):
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
        (aoc.get_input(2015, 20), 786240),
    ],
)
def test_solve(inp, result):
    assert result == solve(inp)
