from __future__ import annotations

import math
from collections.abc import Generator
from typing import NamedTuple

import aoc

Presents = tuple[int, ...]


def equal_split(presents: Presents, target: int) -> tuple[Presents, Presents] | None:
    # don't care if there's multiple possible arrangements.
    # all arrangements of presents 2 and 3 are equivalent since
    # the quantum entanglement of the passenger presents would be the same

    if max(presents) > target or sum(presents) // 2 != target:
        return None

    def _split_helper(
        presents2=(), present2_sum=0, presents3=(), present3_sum=0, presents_index=0,
    ):
        # breakpoint()
        if presents_index == len(presents):
            if present2_sum == target and present3_sum == target:
                return presents2, presents3
            else:
                return None
        elif present2_sum > target or present3_sum > target:
            return None

        for i in range(presents_index, len(presents)):
            split = _split_helper(
                presents2 + (presents[i],),
                present2_sum + presents[i],
                presents3,
                present3_sum,
                i + 1,
            )
            if split is not None:
                return split
            presents3 += (presents[i],)
            present3_sum += presents[i]

        return _split_helper(
            presents2, present2_sum, presents3, present3_sum, len(presents),
        )

    return _split_helper()


def partitions(presents: Presents, size: int) -> Generator[tuple[Presents, Presents]]:
    n = len(presents)
    if size > n:
        return
    indices = list(range(size))

    yield tuple(presents[i] for i in indices), tuple(
        presents[i] for i in range(n) if i not in indices
    )
    while True:
        for i in reversed(range(size)):
            if indices[i] != i + n - size:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, size):
            indices[j] = indices[j - 1] + 1
        yield tuple(presents[i] for i in indices), tuple(
            presents[i] for i in range(n) if i not in indices
        )


class Sleigh(NamedTuple):
    bag1: tuple[int, ...]
    bag2: tuple[int, ...]
    bag3: tuple[int, ...]


def quantum_entanglement(presents: Presents) -> int:
    return math.prod(presents)


def solve(inp: str) -> int:
    presents = tuple(map(int, inp.strip().splitlines()))
    presents = tuple(sorted(presents, reverse=True))

    for bag1_size in range(1, len(presents) - 2):
        sleighs: list[Sleigh] = []
        for bag1, rest in partitions(presents, bag1_size):
            rest_split = equal_split(rest, sum(bag1))
            if rest_split is not None:
                bag2, bag3 = rest_split
                sleighs.append(Sleigh(bag1, bag2, bag3))

        if sleighs:
            sleighs.sort(key=lambda s: quantum_entanglement(s.bag1))
            return quantum_entanglement(sleighs[0].bag1)

    raise AssertionError("There must be an answer.")


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 24),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "presents,target,split",
    [
        ((10, 8, 7, 5, 4, 3, 2, 1), 20, ((10, 8, 2), (7, 5, 4, 3, 1))),
        ((11, 8, 7, 5, 4, 3, 2), 20, ((11, 7, 2), (8, 5, 4, 3))),
        ((11, 9, 7, 5, 4, 3, 1), 20, ((11, 9), (7, 5, 4, 3, 1))),
        ((4, 3, 2, 1), 7, None),
        ((15, 4, 3, 2), 4, None),
    ],
)
def test_equal_split(presents, target, split):
    assert equal_split(presents, target) == split


@pytest.mark.parametrize(
    "presents,presents1_size, results",
    [
        ((1, 2, 3), 1, [((1,), (2, 3)), ((2,), (1, 3)), ((3,), (1, 2))]),
        ((1, 2, 3), 2, [((1, 2), (3,)), ((1, 3), (2,)), ((2, 3), (1,))]),
    ],
)
def test_partitions(presents, presents1_size, results):
    assert list(partitions(presents, presents1_size)) == results


@pytest.mark.parametrize(
    "inp,result",
    [
        ("11\n10\n9\n8\n7\n5\n4\n3\n2\n1\n", 99),
        (aoc.get_input(2015, 24), 10439961859),
    ],
)
def test_solve(inp, result):
    assert result == solve(inp)
