from __future__ import annotations

import re
from itertools import pairwise
from itertools import permutations

import aoc

RE_HAPPY = re.compile(
    r"(\w*) would (gain|lose) (\d*) happiness units by sitting next to (\w*)."
)

HappyMap = dict[tuple[str, str], int]


def parse_relations(relations: str) -> HappyMap:
    happy_map: HappyMap = {}
    for line in relations.strip().splitlines():
        m = RE_HAPPY.fullmatch(line)
        assert m is not None
        happiness = int(m.group(3))
        if m.group(2) == "lose":
            happiness = -happiness
        happy_map[(m.group(1), m.group(4))] = happiness

    return happy_map


def compute_happy_score(arrangement: tuple[str, ...], happy_map: HappyMap) -> int:
    total_happiness = 0
    for pair in pairwise(arrangement):
        total_happiness += happy_map[pair]

    for pair in pairwise(reversed(arrangement)):
        total_happiness += happy_map[pair]

    total_happiness += happy_map[(arrangement[0], arrangement[-1])]
    total_happiness += happy_map[(arrangement[-1], arrangement[0])]

    return total_happiness


def optimize_seating(inp: str) -> int:
    happy_map = parse_relations(inp)
    people = {names[0] for names in happy_map}

    # add myself. i'm apparently neutral
    for person in people:
        happy_map[(person, "myself")] = 0
        happy_map[("myself", person)] = 0
    people.add("myself")

    return max(
        compute_happy_score(arrangement, happy_map)
        for arrangement in permutations(people)
    )


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(optimize_seating, 2015, 13),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "inp,expected_total_happiness",
    [
        (aoc.get_input(2015, 13), 668),
    ],
)
def test_optimize_seating(inp, expected_total_happiness):
    assert expected_total_happiness == optimize_seating(inp)
