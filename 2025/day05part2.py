from __future__ import annotations

from aoc.year2025.day05part1 import _merge_id_ranges
from aoc.year2025.day05part1 import _parse_ingredient_database


def _num_of_available_fresh_ids(id_ranges):
    total = 0
    for id_range in id_ranges:
        total += len(range(id_range[0], id_range[1] + 1))
    return total


def solve(input_s):
    id_ranges, ids = _parse_ingredient_database(input_s)
    id_ranges = _merge_id_ranges(id_ranges)
    available_fresh_ids = _num_of_available_fresh_ids(id_ranges)
    return available_fresh_ids
