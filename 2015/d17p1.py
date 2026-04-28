from __future__ import annotations

from itertools import combinations

import aoc


def eggnog_sets(container_doc: str, eggnog_liters: int = 150) -> int:
    containers = tuple(map(int, container_doc.strip().splitlines()))

    container_combos = 0
    for r in range(1, len(containers)):
        combo_sizes = map(sum, combinations(containers, r))
        combos_right_size = tuple(
            filter(lambda combo: combo == eggnog_liters, combo_sizes)
        )
        container_combos += len(combos_right_size)

    return container_combos


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(eggnog_sets, 2015, 17),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "container_doc,eggnog_liters,container_combos",
    [
        ("20\n15\n10\n5\n5\n", 25, 4),
        (aoc.get_input(2015, 17), 150, 654),
    ],
)
def test_eggnog_sets(container_doc, eggnog_liters, container_combos):
    assert container_combos == eggnog_sets(container_doc, eggnog_liters)
