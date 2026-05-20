from __future__ import annotations

import math
from collections.abc import Generator
from typing import NamedTuple

import aoc

Presents = tuple[int, ...]


def equal_split(
    presents: Presents, target: int, num_bags: int
) -> tuple[Presents, ...] | None:
    # don't care if there's multiple possible arrangements.
    # all arrangements of presents 2 and 3 are equivalent since
    # the quantum entanglement of the passenger presents would be the same

    if max(presents) > target or sum(presents) // num_bags != target:
        return None

    default_bags = ((),) * num_bags

    def _split_helper(bags=default_bags, presents_index=0):
        if presents_index == len(presents):
            for bag in bags:
                if sum(bag) != target:
                    return None
            else:
                return bags

        for bag in bags:
            if sum(bag) > target:
                return None

        for bag_index in range(len(bags)):
            new_bags = list(bags)
            new_bags[bag_index] = new_bags[bag_index] + (presents[presents_index],)
            split = _split_helper(tuple(new_bags), presents_index + 1)

            if split is not None:
                return split

        return None

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
    bag4: tuple[int, ...]


def quantum_entanglement(presents: Presents) -> int:
    return math.prod(presents)


def solve(inp: str) -> int:
    presents = tuple(map(int, inp.strip().splitlines()))
    presents = tuple(sorted(presents, reverse=True))

    for bag1_size in range(1, len(presents) - 2):
        sleighs = []
        for bag1, rest in partitions(presents, bag1_size):
            rest_split = equal_split(rest, sum(bag1), 3)
            if rest_split is not None:
                bag2, bag3, bag4 = rest_split
                sleighs.append(Sleigh(bag1, bag2, bag3, bag4))

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
    "presents,target,num_bags,split",
    [
        ((10, 8, 7, 5, 4, 3, 2, 1), 20, 2, ((10, 8, 2), (7, 5, 4, 3, 1))),
        ((11, 8, 7, 5, 4, 3, 2), 20, 2, ((11, 7, 2), (8, 5, 4, 3))),
        ((11, 9, 7, 5, 4, 3, 1), 20, 2, ((11, 9), (7, 5, 4, 3, 1))),
        ((4, 3, 2, 1), 7, 2, None),
        ((15, 4, 3, 2), 4, 2, None),
    ],
)
def test_equal_split(presents, target, num_bags, split):
    assert equal_split(presents, target, num_bags) == split


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
    [("11\n10\n9\n8\n7\n5\n4\n3\n2\n1\n", 44), (aoc.get_input(2015, 24), 72050269)],
)
def test_solve(inp, result):
    assert result == solve(inp)
