from __future__ import annotations

from collections import Counter
from enum import StrEnum
from typing import NamedTuple

import aoc


class Dir(StrEnum):
    Up = "^"
    Down = "v"
    Left = "<"
    Right = ">"


class Position(NamedTuple):
    x: int
    y: int

    def move(self, direction: Dir) -> Position:
        if direction == Dir.Up:
            return Position(self.x, self.y + 1)
        elif direction == Dir.Down:
            return Position(self.x, self.y - 1)
        elif direction == Dir.Left:
            return Position(self.x - 1, self.y)
        elif direction == Dir.Right:
            return Position(self.x + 1, self.y)

        raise NotImplementedError()


def deliver_presents(directions: str) -> int:
    # take movement instructions and determine
    # how many houses santa delivers at least one present
    santa = Position(0, 0)
    robo_santa = Position(0, 0)
    position_counts = Counter([santa, robo_santa])
    next_to_move, waiting = santa, robo_santa
    for direction in directions.strip():
        next_to_move = next_to_move.move(Dir(direction))
        position_counts.update([next_to_move])
        next_to_move, waiting = waiting, next_to_move

    homes = len(position_counts)
    return homes


if __name__ == "__main__":
    raise SystemExit(aoc.problem_entry_point(deliver_presents, 2015, 3))


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "start,direction,result",
    [
        (Position(0, 0), Dir.Up, Position(0, 1)),
        (Position(0, 0), Dir.Left, Position(-1, 0)),
        (Position(0, 0), Dir.Right, Position(1, 0)),
        (Position(0, 0), Dir.Down, Position(0, -1)),
        (Position(5, 15), Dir.Left, Position(4, 15)),
        (Position(-20, 60), Dir.Down, Position(-20, 59)),
    ],
)
def test_position_movement(start, direction, result):
    assert start.move(direction) == result


@pytest.mark.parametrize(
    "directions,houses",
    [
        ("^v", 3),
        ("^", 2),
        ("^>v<", 3),
        ("^>v", 3),
        ("^v^v^v^v^v", 11),
        ("^^^^^^", 4),
    ],
)
def test_deliver_presents(directions, houses):
    assert houses == deliver_presents(directions)
