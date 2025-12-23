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


def _read_grid(p):
    # returned grid where 1,1 (col, row) is the top left corner
    with open(p) as fobj:
        lines = fobj.read().strip().split()

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


def _remove_rolls_by_forklift(grid):
    new_grid = copy.deepcopy(grid)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@" and _can_be_accessed_by_forklift(grid, row, col):
                new_grid[row][col] = "."
            else:
                new_grid[row][col] = grid[row][col]

    return new_grid


def _num_rolls_access_by_forklift_with_removal(grid):
    count = 0
    while step_count := _num_rolls_access_by_forklift(grid):
        count += step_count
        grid = _remove_rolls_by_forklift(grid)
    return count


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=lambda s: Path(s).absolute())
    args = parser.parse_args(argv)

    grid = _read_grid(args.input)
    print(f"Number of rolls: {_num_rolls_access_by_forklift(grid)}")

    print(
        f"Number of rolls with removal: {_num_rolls_access_by_forklift_with_removal(grid)}"
    )


if __name__ == "__main__":
    raise SystemExit(_main())
