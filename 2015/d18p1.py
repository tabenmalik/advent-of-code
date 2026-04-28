from __future__ import annotations

import aoc

GridData = tuple[tuple[str, ...], ...]


def buffer_grid(grid: GridData) -> GridData:
    grid_lists = [list(row) for row in grid]

    grid_lists.insert(0, ["."] * len(grid_lists))
    grid_lists.append(["."] * len(grid_lists))

    for row in grid_lists:
        row.insert(0, ".")
        row.append(".")

    return tuple(tuple(row) for row in grid_lists)


def update_light(grid: GridData, row: int, col: int) -> str:
    neighbors_on = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            if grid[row + i][col + j] == "#":
                neighbors_on += 1

    curr_light = grid[row][col]
    if curr_light == "#" and neighbors_on in {2, 3}:
        return "#"
    elif curr_light == "." and neighbors_on == 3:
        return "#"
    else:
        return "."


class Lights:

    def __init__(self, init_grid: GridData):
        self._grid: GridData = buffer_grid(init_grid)

    def step(self):
        new_grid: list[list[str]] = []

        for row in range(1, len(self._grid) - 1):
            new_grid.append([])
            for col in range(1, len(self._grid[0]) - 1):
                new_light = update_light(self._grid, row, col)
                new_grid[row - 1].append(new_light)

        self._grid = buffer_grid(tuple(map(tuple, new_grid)))

    def num_on(self):
        return len(tuple(True for row in self._grid for item in row if item == "#"))


def conway_game_of_lights(init_config: str, steps: int = 100) -> int:
    grid_data: GridData = tuple(
        tuple(line) for line in init_config.strip().splitlines()
    )

    lights = Lights(grid_data)

    for _ in range(steps):
        lights.step()

    return lights.num_on()


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(conway_game_of_lights, 2015, 18),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "init_config,steps,lights_on",
    [
        (
            ".#.#.#\n...##.\n#....#\n..#...\n#.#..#\n####..\n",
            4,
            4,
        ),
        (aoc.get_input(2015, 18), 100, 814),
    ],
)
def test_conway_game_of_lights(init_config, steps, lights_on):
    assert lights_on == conway_game_of_lights(init_config, steps)
