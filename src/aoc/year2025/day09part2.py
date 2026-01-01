from __future__ import annotations

from itertools import chain
from itertools import combinations
from itertools import pairwise
from math import copysign
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


def is_horizontal(ray: tuple[Point, Point]):
    return ray[0].y == ray[1].y


def intersect(ray: tuple[Point, Point], p: Point) -> bool:
    if is_horizontal(ray):
        return False
    return (
        p.x >= ray[0].x
        and max(ray[0].y, ray[1].y) >= p.y
        and p.y > min(ray[0].y, ray[1].y)
    )


def on_line(ray: tuple[Point, Point], p: Point) -> bool:
    if (
        is_horizontal(ray)
        and p.y == ray[0].y
        and max(ray[0].x, ray[1].x) >= p.x
        and p.x >= min(ray[0].x, ray[1].x)
    ):
        return True
    return (
        p.x == ray[0].x
        and max(ray[0].y, ray[1].y) >= p.y
        and p.y >= min(ray[0].y, ray[1].y)
    )


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_csv(cls, s):
        return cls(*map(int, s.strip().split(",")))


def ray_points(ray):
    step = (0, int(copysign(1, ray[1].y - ray[0].y)))
    if is_horizontal(ray):
        step = (int(copysign(1, ray[1].x - ray[0].x)), 0)

    p = ray[0]
    while p != ray[1]:
        yield p
        p = Point(p.x + step[0], p.y + step[1])


class Rectangle(NamedTuple):

    corners: tuple[Point, Point, Point, Point]

    @classmethod
    def from_two_points(cls, p1, p3):
        p2 = Point(p1.x - (p1.x - p3.x), p1.y)
        p4 = Point(p1.x, p1.y - (p1.y - p3.y))
        return cls((p1, p2, p3, p4))

    def area(self):
        p1 = self.corners[0]
        p3 = self.corners[2]
        return int((abs(p1.x - p3.x) + 1) * (abs(p1.y - p3.y) + 1))

    def perimeter_points(self):
        for ray in pairwise(chain(self.corners, (self.corners[0],))):
            yield from ray_points(ray)


class Polygon(NamedTuple):
    points: tuple[Point]

    def contains(self, rec: Rectangle) -> bool:
        for point in rec.perimeter_points():
            if not self.contains_point(point):
                return False
        return True

    def contains_point(self, point) -> bool:
        intersect_count = 0
        for ray in pairwise(chain(self.points, (self.points[0],))):
            if on_line(ray, point):
                return True
            if intersect(ray, point):
                intersect_count += 1
        return intersect_count % 2 != 0

    @classmethod
    def from_csv(cls, csv):
        points = [Point.from_csv(line) for line in csv.strip().split("\n")]

        return cls(points)


def _parse_points(input_s):
    return tuple(map(Point.from_csv, input_s.strip().split("\n")))


def _max_area(points):
    polygon = Polygon(points)

    max_area = 0
    rects = [Rectangle.from_two_points(p1, p2) for p1, p2 in combinations(points, 2)]
    rects.sort(key=Rectangle.area, reverse=True)

    for rect in rects:
        print(rect)
        if polygon.contains(rect):
            return rect.area()

    return max_area


def solve(input_s) -> int:

    points = _parse_points(input_s)

    return _max_area(points)


@pytest.mark.parametrize("input_s", [EXAMPLE])
def test_solve(input_s):
    assert solve(input_s) == 24


@pytest.mark.parametrize(
    "polygon, point",
    [
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(2, 2)),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(1, 0)),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(1, 3)),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(3, 2)),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(2, 0)),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(0, 0)),
        (Polygon.from_csv("0,0\n4,0\n4,3\n2,3\n2,1\n1,1\n1,3\n0,3\n"), Point(3, 2)),
        (Polygon.from_csv("0,0\n4,0\n4,3\n2,3\n2,1\n1,1\n1,3\n0,3\n"), Point(3, 1)),
    ],
)
def test_contains_point(polygon, point):
    assert polygon.contains_point(point)


@pytest.mark.parametrize(
    "polygon, point",
    [
        (Polygon.from_csv("1,0\n4,0\n4,3\n1,3\n"), Point.from_csv("0,2")),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point.from_csv("1,4")),
        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point.from_csv("4,2")),
        (
            Polygon.from_csv("0,0\n4,0\n4,3\n3,3\n3,1\n1,1\n1,4\n0,4\n"),
            Point.from_csv("2,2"),
        ),
        (
            Polygon.from_csv("0,0\n4,0\n4,3\n3,3\n3,1\n1,1\n1,4\n0,4\n"),
            Point.from_csv("2,3"),
        ),
    ],
)
def test_not_contains_point(polygon, point):
    assert not polygon.contains_point(point)


@pytest.mark.parametrize(
    "ray, point",
    [
        ((Point(1, 1), Point(1, 5)), Point(3, 3)),
        ((Point(1, 5), Point(1, 1)), Point(3, 3)),
        ((Point(1, 1), Point(1, 5)), Point(1, 5)),
        ((Point(1, 5), Point(1, 1)), Point(1, 5)),
        ((Point(1, 1), Point(1, 5)), Point(1, 5)),
        ((Point(1, 5), Point(1, 1)), Point(1, 5)),
        ((Point(0, 0), Point(0, 4)), Point(0, 3)),
        ((Point(0, 4), Point(0, 0)), Point(0, 3)),
    ],
)
def test_intersects(ray, point):
    assert intersect(ray, point)


@pytest.mark.parametrize(
    "ray, point",
    [
        ((Point(1, 1), Point(1, 5)), Point(0, 4)),
        ((Point(1, 5), Point(1, 1)), Point(0, 4)),
        ((Point(1, 1), Point(1, 5)), Point(3, 6)),
        ((Point(1, 1), Point(4, 1)), Point(4, 2)),
        ((Point(4, 1), Point(1, 1)), Point(4, 2)),
        ((Point(1, 1), Point(4, 1)), Point(4, 1)),
        ((Point(4, 1), Point(1, 1)), Point(4, 1)),
        ((Point(0, 0), Point(4, 0)), Point(0, 0)),
        ((Point(4, 0), Point(0, 0)), Point(0, 0)),
    ],
)
def test_not_intersects(ray, point):
    assert not intersect(ray, point)
