from __future__ import annotations

import copy

from aoc.year2025.day04part1 import _can_be_accessed_by_forklift
from aoc.year2025.day04part1 import _num_rolls_access_by_forklift
from aoc.year2025.day04part1 import _parse_grid


def _num_rolls_access_by_forklift_with_removal(grid):
    count = 0
    while step_count := _num_rolls_access_by_forklift(grid):
        count += step_count
        grid = _remove_rolls_by_forklift(grid)
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


def solve(input_s):
    grid = _parse_grid(input_s)
    return _num_rolls_access_by_forklift_with_removal(grid)
