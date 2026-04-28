from __future__ import annotations

from itertools import combinations

import aoc


def eggnog_sets(container_doc: str, eggnog_liters: int = 150) -> int:
    containers = tuple(map(int, container_doc.strip().splitlines()))

    # group container combos by the number of containers
    container_combos: dict[int, list[tuple[int, ...]]] = {}

    for r in range(1, len(containers)):
        for combo in combinations(containers, r):
            if sum(combo) == eggnog_liters:
                container_combos.setdefault(len(combo), []).append(combo)

    smallest_combo_size = min(container_combos.keys())
    return len(container_combos[smallest_combo_size])


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(eggnog_sets, 2015, 17),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "container_doc,eggnog_liters,container_combos",
    [
        ("20\n15\n10\n5\n5\n", 25, 3),
        (aoc.get_input(2015, 17), 150, 57),
    ],
)
def test_eggnog_sets(container_doc, eggnog_liters, container_combos):
    assert container_combos == eggnog_sets(container_doc, eggnog_liters)
