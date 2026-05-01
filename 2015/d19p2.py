from __future__ import annotations

import re
from typing import NamedTuple

import aoc


class Replacement(NamedTuple):
    og: str
    sub: str


def all_next_molecules(
    molecule: str, replacements: tuple[Replacement, ...]
) -> set[str]:
    new_molecules: set[str] = set()
    for replacement in replacements:
        for m in re.finditer(replacement.og, molecule):
            start, stop = m.span()
            new_molecule = "".join([molecule[:start], replacement.sub, molecule[stop:]])
            new_molecules.add(new_molecule)

    return new_molecules


def build_molecule(inp: str) -> int:
    # solved on intuition but not confident that it is provably
    # a general solution. search for the optimal substitutions
    # by working backwards from the target molecule and applying
    # the reverse replacements. Always pick the shortest molecule
    # next to continue the search. As the molecule length shortens
    # and has fewer possible replacements to make the growth of
    # molecules to check will decrease.
    repl_inp, end_molecule = inp.strip().split("\n\n")
    repls = tuple(
        Replacement(*reversed(line.split(" => "))) for line in repl_inp.split("\n")
    )
    repls = tuple(sorted(repls, key=lambda repl: len(repl.og), reverse=True))

    molecules: set[str] = {end_molecule}
    molecule_count: dict[str, int] = {end_molecule: 0}
    while True:
        # find the shortest molecule
        molecule = min(molecules, key=len)
        molecules.remove(molecule)
        count = molecule_count.pop(molecule) + 1

        new_molecules = all_next_molecules(molecule, repls)
        if "e" in new_molecules:
            return count

        molecules.update(new_molecules)
        molecule_count.update({m: count for m in molecules})


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(build_molecule, 2015, 19),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "inp,num_molecules",
    [
        (
            "e => H\ne => O\nH => HO\nH => OH\nO => HH\n\nHOH\n",
            3,
        ),
        (
            "e => H\ne => O\nH => HO\nH => OH\nO => HH\n\nHOHOHO\n",
            6,
        ),
        (aoc.get_input(2015, 19), 200),
    ],
)
def test_build_molecule(inp, num_molecules):
    assert num_molecules == build_molecule(inp)
