from __future__ import annotations

from itertools import combinations
from typing import NamedTuple

import pytest

EXAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_csv(cls, s):
        return cls(*map(int, s.strip().split(",")))


def _parse_points(input_s):
    return tuple(map(Point.from_csv, input_s.strip().split("\n")))


def area(p1, p2):
    return int(abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1))


def _largest_rect(points):
    max_area = 0
    max_area_pair = None

    for pair in combinations(points, 2):
        a = area(*pair)
        if a > max_area:
            max_area = a
            max_area_pair = pair

    return max_area


def solve(input_s) -> int:

    points = _parse_points(input_s)

    return _largest_rect(points)


@pytest.mark.parametrize("input_s", [EXAMPLE])
def test_solve(input_s):
    assert solve(input_s) == 50
