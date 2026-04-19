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


def wrapping_paper_for_box(box: Box) -> int:
    square_feet = (
        2 * box.length * box.width
        + 2 * box.length * box.height
        + 2 * box.width * box.height
    )

    # find the smallest side of box by getting the two
    # smallest dimensions of the box
    l, w, _ = sorted(box)
    square_feet += l * w

    return square_feet


def total_wrapping_paper(box_lines: str) -> int:
    boxes: list[Box] = []
    for box_line in box_lines.splitlines():
        boxes.append(parse_box(box_line))

    total_square_feet = 0
    for box in boxes:
        total_square_feet += wrapping_paper_for_box(box)
    return total_square_feet


if __name__ == "__main__":
    raise SystemExit(problem_entry_point(total_wrapping_paper, 2015, 2))


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "dimensions,total",
    [
        ("2x3x4\n", 58),
        # similar but different order
        ("3x4x2\n", 58),
        ("1x1x10\n", 43),
        ("2x3x4\n1x1x10\n", 101),
        (get_input(2015, 2), 1606483),
    ],
)
def test_total_wrapping_paper(dimensions, total):
    assert total_wrapping_paper(dimensions) == total
