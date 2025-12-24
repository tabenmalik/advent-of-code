from __future__ import annotations

from aoc.year2025.day07part1 import _parse_tachyon_manifold


def solve(input_s):
    tm = _parse_tachyon_manifold(input_s)
    while tm.can_update():
        tm.update()
    return tm.total_timelines()
