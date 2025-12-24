from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Sequence

EXAMPLE = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def _parse_grid(input_s):
    # returned grid where 1,1 (col, row) is the top left corner
    lines = input_s.strip().split()

    # Adding a buffer around the grid to simplify later checks.
    num_cols = len(lines[0])
    extra_row = "." * num_cols
    lines.insert(0, extra_row)
    lines.append(extra_row)
    lines = ["." + line + "." for line in lines]

    grid = [list(line) for line in lines]

    return grid


def _num_adjacent_rolls(grid, center_row, center_col):
    count = 0
    for row in [center_row - 1, center_row, center_row + 1]:
        for col in [center_col - 1, center_col, center_col + 1]:
            if row == center_row and col == center_col:
                continue

            if grid[row][col] == "@":
                count += 1
    return count


def _can_be_accessed_by_forklift(grid, center_row, center_col):
    return _num_adjacent_rolls(grid, center_row, center_col) < 4


def _num_rolls_access_by_forklift(grid):
    count = 0
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            if grid[row][col] == "@" and _can_be_accessed_by_forklift(grid, row, col):
                count += 1
    return count


def solve(input_s):
    grid = _parse_grid(input_s)
    return _num_rolls_access_by_forklift(grid)
