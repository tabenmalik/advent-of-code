from __future__ import annotations

import re
from typing import NamedTuple

import aoc


class Replacement(NamedTuple):
    og: str
    sub: str


def count_molecules(inp: str) -> int:
    repl_inp, start_molecule = inp.strip().split("\n\n")
    replacements = tuple(
        Replacement(*line.split(" => ")) for line in repl_inp.split("\n")
    )

    new_molecules: set[str] = set()
    for replacement in replacements:
        for m in re.finditer(replacement.og, start_molecule):
            start, stop = m.span()
            new_molecule = "".join(
                [start_molecule[:start], replacement.sub, start_molecule[stop:]]
            )
            new_molecules.add(new_molecule)

    return len(new_molecules)


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(count_molecules, 2015, 19),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "inp,num_molecules",
    [
        (
            "H => HO\nH => OH\nO => HH\n\nHOH\n",
            4,
        ),
        (
            "H => HO\nH => OH\nO => HH\n\nHOHOHO\n",
            7,
        ),
        (
            "H => HO\n\nNO\n",
            0,
        ),
        (
            "Abc => t\n\nxyAbcabc\n",
            1,
        ),
        (aoc.get_input(2015, 19), 518),
    ],
)
def test_count_molecules(inp, num_molecules):
    assert num_molecules == count_molecules(inp)
