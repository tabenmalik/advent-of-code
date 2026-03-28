from __future__ import annotations

from typing import NamedTuple

from aoc import get_input
from aoc import problem_entry_point


class Box(NamedTuple):
    length: int
    width: int
    height: int


def parse_box(dims: str) -> Box:
    l, w, h = dims.split("x")
    return Box(int(l), int(w), int(h))


def ribbon_length_for_box(box: Box) -> int:
    # shortest distance around its side can be
    # found by taking the two shortest dimensions of the box
    l, w, h = sorted(box)

    # for wrapping the present
    ribbon = 2 * l + 2 * w
    # for the bow
    ribbon += l * w * h
    return ribbon


def total_ribbon_length(box_lines: str) -> int:
    boxes: list[Box] = []
    for box_line in box_lines.splitlines():
        boxes.append(parse_box(box_line))

    total_ribbon_feet = 0
    for box in boxes:
        total_ribbon_feet += ribbon_length_for_box(box)
    return total_ribbon_feet


if __name__ == "__main__":
    raise SystemExit(problem_entry_point(total_ribbon_length, 2015, 2))


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "dimensions,total",
    [
        ("2x3x4\n", 34),
        # similar but different order
        ("3x4x2\n", 34),
        ("1x1x10\n", 14),
        ("2x3x4\n1x1x10\n", 48),
        (get_input(2015, 2), 3842356),
    ],
)
def test_total_wrapping_paper(dimensions, total):
    assert total_ribbon_length(dimensions) == total
