from __future__ import annotations

EXAMPLE = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


class TachyonManifold:

    def __init__(self, manifold_array: list[list[str]]):
        self._data = manifold_array
        self._beams = {self._find_start(self._data)}
        self._timelines = {self._find_start(self._data): 1}

    def __getitem__(self, loc: tuple[int, int]) -> str:
        return self._data[loc[0]][loc[1]]

    def __setitem__(self, loc: tuple[int, int], v: str) -> None:
        self._data[loc[0]][loc[1]] = v

    @staticmethod
    def _find_start(manifold_array: list[list[str]]) -> tuple[int, int]:
        for row in range(len(manifold_array)):
            for col in range(len(manifold_array[0])):
                if manifold_array[row][col] == "S":
                    return (row, col)
        assert False, "There must be a starting point"

    def __str__(self) -> str:
        return "\n".join(map("".join, self._data)) + "\n"

    def num_splits(self) -> int:
        total = 0
        for row in range(len(self._data)):
            for col in range(len(self._data[0])):
                if (
                    self._data[row][col] == "^"
                    and self._data[row - 1][col] == "|"
                ):
                    total += 1
        return total

    def total_timelines(self) -> int:
        return sum(self._timelines.values())

    def can_update(self) -> bool:
        return len(self._beams) > 0

    def update(self) -> None:
        # copy the beam set since it will be modified in the loop
        for beam_loc in list(self._beams):
            below_loc = beam_loc[0] + 1, beam_loc[1]
            below_left = below_loc[0], below_loc[1] - 1
            below_right = below_loc[0], below_loc[1] + 1

            # Reached the end, remove from list
            if beam_loc[0] + 1 >= len(self._data):
                self._beams.remove(beam_loc)
            # Empty space below, add a new beam
            elif self[below_loc] == ".":
                self[below_loc] = "|"
                self._beams.remove(beam_loc)
                self._beams.add(below_loc)
                self._timelines[below_loc] = self._timelines.pop(beam_loc)
            # Splitter beneath, split the beam, add timeline
            elif self[below_loc] == "^":
                self._beams.remove(beam_loc)
                self[below_right] = "|"
                self[below_left] = "|"
                # self._beams is a set so no worries of duplicate beams
                self._beams.add(below_right)
                self._beams.add(below_left)
                t = self._timelines.pop(beam_loc)
                self._timelines[below_right] = self._timelines.pop(
                    below_right, 0,
                ) + t
                self._timelines[below_left] = self._timelines.pop(
                    below_left, 0,
                ) + t
            # Another beam below
            elif self[below_loc] == "|":
                self._beams.remove(beam_loc)
                self._timelines[below_loc] += self._timelines.pop(beam_loc)
            else:
                assert False, "Shouldn't happen!"


def _parse_tachyon_manifold(input_s: str) -> TachyonManifold:
    return TachyonManifold(list(map(list, input_s.strip().split())))


def solve(input_s: str) -> int:
    tm = _parse_tachyon_manifold(input_s)
    while tm.can_update():
        tm.update()
    return tm.total_timelines()
