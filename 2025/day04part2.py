from __future__ import annotations

import copy
from typing import TypeAlias

Grid: TypeAlias = list[list[str]]


def _parse_grid(input_s: str) -> Grid:
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


def _num_rolls_access_by_forklift(grid: Grid) -> int:
    count = 0
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            if (
                grid[row][col] == "@"
                and _can_be_accessed_by_forklift(grid, row, col)
            ):
                count += 1
    return count


def _num_adjacent_rolls(grid: Grid, center_row: int, center_col: int) -> int:
    count = 0
    for row in [center_row - 1, center_row, center_row + 1]:
        for col in [center_col - 1, center_col, center_col + 1]:
            if row == center_row and col == center_col:
                continue

            if grid[row][col] == "@":
                count += 1
    return count


def _can_be_accessed_by_forklift(
    grid: Grid,
    center_row: int,
    center_col: int,
) -> bool:
    return _num_adjacent_rolls(grid, center_row, center_col) < 4


def _num_rolls_access_by_forklift_with_removal(grid: Grid) -> int:
    count = 0
    while step_count := _num_rolls_access_by_forklift(grid):
        count += step_count
        grid = _remove_rolls_by_forklift(grid)
    return count


def _remove_rolls_by_forklift(grid: Grid) -> Grid:
    new_grid = copy.deepcopy(grid)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (
                grid[row][col] == "@"
                and _can_be_accessed_by_forklift(grid, row, col)
            ):
                new_grid[row][col] = "."
            else:
                new_grid[row][col] = grid[row][col]

    return new_grid


def solve(input_s: str) -> int:
    grid = _parse_grid(input_s)
    return _num_rolls_access_by_forklift_with_removal(grid)
