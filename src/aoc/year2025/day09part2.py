from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import cache
from functools import cached_property
from itertools import chain
from itertools import combinations
from itertools import pairwise
from itertools import product
from math import copysign
from typing import NamedTuple

import pytest

# need a different approach
# compute all internal polygon points
# then for each rectangle:
#   if all corners in polygon points
#   and then all rect perimeter points are in polygon
#   then check if max area

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


@cache
def is_horizontal(ray: tuple[Point, Point]):
    return ray[0].y == ray[1].y


def intersect_vertical(ray: tuple[Point, Point], p: Point) -> bool:
    return (
        p.x >= ray[0].x
        and max(ray[0].y, ray[1].y) >= p.y
        and p.y > min(ray[0].y, ray[1].y)
    )


def intersects(r1, r2) -> bool:
    if is_horizontal(r1) == is_horizontal(r2):
        return False
    if is_horizontal(r1):
        return (
            max(r1[0].x, r1[1].x) >= r2[0].x
            and r2[0].x > min(r1[0].x, r1[1].x)
            and max(r2[0].y, r2[1].y) >= r1[0].y
            and r1[0].y > min(r2[0].y, r2[1].y)
        )
    return (
        max(r1[0].y, r1[1].y) >= r2[0].y
        and r2[0].y > min(r1[0].y, r1[1].y)
        and max(r2[0].x, r2[1].x) >= r1[0].x
        and r1[0].x > min(r2[0].x, r2[1].x)
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

    def rays(self):
        yield from pairwise(chain(self.corners, (self.corners[0],)))


@dataclass(frozen=True)
class Polygon:
    points: tuple[Point]

    def contains(self, rec: Rectangle) -> bool:
        intersect_count = 0
        for rec_ray in rec.rays():
            for poly_ray in self.rays:
                if intersects(rec_ray, poly_ray):
                    intersect_count += 1
        return intersect_count % 2 != 0

        for point in rec.perimeter_points():
            if not self.contains_point(point):
                return False
        return True

    @cached_property
    def rays(self):
        return tuple(pairwise(chain(self.points, (self.points[0],))))

    @cached_property
    def vertical_rays(self):
        return tuple(ray for ray in self.rays if not is_horizontal(ray))

    @cached_property
    def perimeter_points(self) -> tuple:
        return tuple(point for ray in self.rays for point in ray_points(ray))

    def __str__(self):
        min_x = min(p.x for p in self.points) - 1
        max_x = max(p.x for p in self.points) + 1
        min_y = min(p.y for p in self.points) - 1
        max_y = max(p.y for p in self.points) + 1

        chars = []
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if Point(x, y) in self.points:
                    chars.append("#")
                elif Point(x, y) in self.all_points:
                    chars.append("X")
                else:
                    chars.append(".")
            chars.append("\n")
        return "".join(chars)

    @cached_property
    def all_points(self):
        all_points = set(self.perimeter_points)

        min_x = min(p.x for p in self.points) - 1
        max_x = max(p.x for p in self.points) + 1
        min_y = min(p.y for p in self.points) - 1
        max_y = max(p.y for p in self.points) + 1

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if Point(x, y) in self.perimeter_points:
                    continue

        return all_points

    def contains_point(self, point) -> bool:
        intersect_count = 0
        if point in self.perimeter_points:
            return True

        for ray in self.vertical_rays:
            if intersect_vertical(ray, point):
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


@dataclass
class TileChunk:
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    outside: bool | None = None

    def contains_point(self, p):
        return (
            self.x_range[1] > p.x
            and p.x >= self.x_range[0]
            and self.y_range[1] > p.y
            and p.y >= self.y_range[0]
        )


def flood_fill(chunk_grid):
    to_check = deque()
    to_check.append((0, 0))

    while to_check:
        x, y = to_check.pop()
        chunk_grid[x][y].outside = True
        for move in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            next_x, next_y = x + move[0], y + move[1]

            if next_x < 0 or next_x >= len(chunk_grid):
                continue

            if next_y < 0 or next_y >= len(chunk_grid[0]):
                continue

            if chunk_grid[next_x][next_y].outside is None:
                to_check.append((next_x, next_y))


def find_chunk(chunk_grid, point):
    for x in range(len(chunk_grid)):
        if (
            chunk_grid[x][0].x_range[0] <= point.x
            and point.x < chunk_grid[x][0].x_range[1]
        ):
            break

    for y in range(len(chunk_grid)):
        if (
            chunk_grid[x][y].y_range[0] <= point.y
            and point.y < chunk_grid[x][y].y_range[1]
        ):
            break

    return x, y


def solve(input_s) -> int:

    red_tiles = _parse_points(input_s)

    x_lines = list({tile.x for tile in red_tiles})
    x_lines += [x_line + 1 for x_line in x_lines]
    x_lines += [0, max(x_lines) + 1]
    x_lines.sort()

    y_lines = list({tile.y for tile in red_tiles})
    y_lines += [y_line + 1 for y_line in y_lines]
    y_lines += [0, max(y_lines) + 1]
    y_lines.sort()

    perimeter_points = tuple(
        point
        for ray in pairwise(chain(red_tiles, (red_tiles[0],)))
        for point in ray_points(ray)
    )
    perimeter_point_set = set(perimeter_points)

    chunk_grid = []
    for x_range in pairwise(x_lines):
        chunk_grid.append([])
        for y_range in pairwise(y_lines):
            tc = TileChunk(x_range, y_range)
            if Point(x_range[0], y_range[0]) in perimeter_point_set:
                tc.outside = False
            chunk_grid[-1].append(tc)

    flood_fill(chunk_grid)

    rectangles = [
        Rectangle.from_two_points(p1, p3) for p1, p3 in combinations(red_tiles, 2)
    ]
    rectangles.sort(key=Rectangle.area, reverse=True)
    for rect in rectangles:
        print(rect)
        corner_chunk_ind = []
        disqualified = False

        for corner in rect.corners:
            x, y = find_chunk(chunk_grid, corner)
            if chunk_grid[x][y].outside:
                disqualified = True
                break
            else:
                corner_chunk_ind.append(chunk_grid[x][y])

        if disqualified:
            continue

        corner_chunk_ind.sort(key=lambda tc: (tc.x_range, tc.y_range))
        print(corner_chunk_ind)

        first_xy = None
        last_xy = None
        for x, y in product(range(len(chunk_grid)), range(len(chunk_grid[0]))):
            if chunk_grid[x][y] == corner_chunk_ind[0]:
                first_xy = (x, y)
            elif chunk_grid[x][y] == corner_chunk_ind[1]:
                last_xy = (x, y)

            if first_xy is not None and last_xy is not None:
                break

        for x, y in product(
            range(first_xy[0], last_xy[0] + 1), range(first_xy[1], last_xy[1])
        ):
            print(chunk_grid[x][y])
            if chunk_grid[x][y].outside:
                print("disqualified")
                disqualified = True
                break

        if disqualified:
            continue

        break

    return rect.area()


@pytest.mark.parametrize("input_s", [EXAMPLE])
def test_solve(input_s):
    assert solve(input_s) == 24


# @pytest.mark.parametrize(
#    "polygon, point",
#    [
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(2, 2)),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(1, 0)),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(1, 3)),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(3, 2)),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(2, 0)),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point(0, 0)),
#        (Polygon.from_csv("0,0\n4,0\n4,3\n2,3\n2,1\n1,1\n1,3\n0,3\n"), Point(3, 2)),
#        (Polygon.from_csv("0,0\n4,0\n4,3\n2,3\n2,1\n1,1\n1,3\n0,3\n"), Point(3, 1)),
#    ],
# )
# def test_contains_point(polygon, point):
#    assert polygon.contains_point(point)
#
#
# @pytest.mark.parametrize(
#    "polygon, point",
#    [
#        (Polygon.from_csv("1,0\n4,0\n4,3\n1,3\n"), Point.from_csv("0,2")),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point.from_csv("1,4")),
#        (Polygon.from_csv("0,0\n3,0\n3,3\n0,3\n"), Point.from_csv("4,2")),
#        (
#            Polygon.from_csv("0,0\n4,0\n4,3\n3,3\n3,1\n1,1\n1,4\n0,4\n"),
#            Point.from_csv("2,2"),
#        ),
#        (
#            Polygon.from_csv("0,0\n4,0\n4,3\n3,3\n3,1\n1,1\n1,4\n0,4\n"),
#            Point.from_csv("2,3"),
#        ),
#    ],
# )
# def test_not_contains_point(polygon, point):
#    assert not polygon.contains_point(point)
#
#
# @pytest.mark.parametrize(
#    "ray, point",
#    [
#        ((Point(1, 1), Point(1, 5)), Point(3, 3)),
#        ((Point(1, 5), Point(1, 1)), Point(3, 3)),
#        ((Point(1, 1), Point(1, 5)), Point(1, 5)),
#        ((Point(1, 5), Point(1, 1)), Point(1, 5)),
#        ((Point(1, 1), Point(1, 5)), Point(1, 5)),
#        ((Point(1, 5), Point(1, 1)), Point(1, 5)),
#        ((Point(0, 0), Point(0, 4)), Point(0, 3)),
#        ((Point(0, 4), Point(0, 0)), Point(0, 3)),
#    ],
# )
# def test_intersects(ray, point):
#    assert intersect_vertical(ray, point)
#
#
# @pytest.mark.parametrize(
#    "ray, point",
#    [
#        ((Point(1, 1), Point(1, 5)), Point(0, 4)),
#        ((Point(1, 5), Point(1, 1)), Point(0, 4)),
#        ((Point(1, 1), Point(1, 5)), Point(3, 6)),
#        ((Point(1, 1), Point(4, 1)), Point(4, 2)),
#        ((Point(4, 1), Point(1, 1)), Point(4, 2)),
#        ((Point(1, 1), Point(4, 1)), Point(4, 1)),
#        ((Point(4, 1), Point(1, 1)), Point(4, 1)),
#        ((Point(0, 0), Point(4, 0)), Point(0, 0)),
#        ((Point(4, 0), Point(0, 0)), Point(0, 0)),
#    ],
# )
# def test_not_intersects(ray, point):
#    assert not intersect_vertical(ray, point)
