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
        (
            "Alice would gain 54 happiness units by sitting next to Bob.\n"
            "Alice would lose 79 happiness units by sitting next to Carol.\n"
            "Alice would lose 2 happiness units by sitting next to David.\n"
            "Bob would gain 83 happiness units by sitting next to Alice.\n"
            "Bob would lose 7 happiness units by sitting next to Carol.\n"
            "Bob would lose 63 happiness units by sitting next to David.\n"
            "Carol would lose 62 happiness units by sitting next to Alice.\n"
            "Carol would gain 60 happiness units by sitting next to Bob.\n"
            "Carol would gain 55 happiness units by sitting next to David.\n"
            "David would gain 46 happiness units by sitting next to Alice.\n"
            "David would lose 7 happiness units by sitting next to Bob.\n"
            "David would gain 41 happiness units by sitting next to Carol.\n",
            330,
        ),
        (aoc.get_input(2015, 13), 709),
    ],
)
def test_optimize_seating(inp, expected_total_happiness):
    assert expected_total_happiness == optimize_seating(inp)
