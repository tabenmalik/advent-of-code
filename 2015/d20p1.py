from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
from itertools import count
from math import isqrt

import aoc


def divisors(n: int) -> Iterator[int]:
    """Return all divisors of `n`. Order not guaranteed."""
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            yield i
            j = n // i
            if j != i:
                yield j


def presents(house: int) -> int:
    """Return the presents that `house` will receive."""
    return sum(divisors(house)) * 10


def solve(inp: str) -> int:
    target_presents = int(inp)

    # Limit the search to only even numbers after house 3.
    # In effect, only the highly abundant numbers need to be
    # checked. It's not practical to generate the sequence
    # of highly abundant numbers but the numbers to search
    # can be cut almost in half due to the property that all
    # highly abundant numbers above 3 are even.
    # What a time saver!
    #
    # Why must the answer be a highly abundant number?
    # The sum-of-divisors is not a monotonically
    # increasing sequence. The highly abundant numbers are the
    # "record" peaks in the sequence, a subset that *is* monotonically
    # inceasing. So a house with a highly abundant number is guaranteed
    # to be the first house that has at least X pesents.
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
        ("10\n", 1),
        ("20\n", 2),
        ("80\n", 6),
        ("150\n", 8),
        (aoc.get_input(2015, 20), 776160),
    ],
)
def test_solve(inp, result):
    assert result == solve(inp)
