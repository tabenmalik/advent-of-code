from __future__ import annotations

import re
from collections.abc import Callable
from itertools import chain
from itertools import product
from math import copysign
from typing import NamedTuple

import aoc

RE_INSTRUCTION = re.compile(
    r"^(?P<inst>turn on|toggle|turn off) (?P<row1>\d+),(?P<col1>\d+) through (?P<row2>\d+),(?P<col2>\d+)$"  # noqa: E501
)


def turn_on(val: int) -> int:
    return val + 1


def turn_off(val: int) -> int:
    return max(0, val - 1)


def toggle(val: int) -> int:
    return val + 2


class LightOp(NamedTuple):
    op: Callable[[int], int]
    rows: range
    cols: range


def parse_instruction(line: str) -> LightOp:
    m = RE_INSTRUCTION.search(line)
    if not m:
        raise ValueError(f"not a valid instruction: {line=}")

    op: Callable[[int], int] = turn_on
    if m.group("inst") == "turn on":
        op = turn_on
    elif m.group("inst") == "toggle":
        op = toggle
    elif m.group("inst") == "turn off":
        op = turn_off
    else:
        raise NotImplementedError()

    row_step = int(copysign(1, int(m.group("row2")) - int(m.group("row1")) + 1))
    rows = range(int(m.group("row1")), int(m.group("row2")) + row_step, row_step)

    col_step = int(copysign(1, int(m.group("col2")) - int(m.group("col1")) + 1))
    cols = range(int(m.group("col1")), int(m.group("col2")) + col_step, col_step)

    return LightOp(op, rows, cols)


def configure_lights(instructions: str) -> int:
    lights = [[0 for _ in range(0, 1000)] for _ in range(0, 1000)]
    for line in instructions.strip().splitlines():
        light_op = parse_instruction(line)
        for row, col in product(light_op.rows, light_op.cols):
            lights[row][col] = light_op.op(lights[row][col])

    total_brightness = sum(chain.from_iterable(lights))
    return total_brightness


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(configure_lights, 2015, 6),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "instruction_string,instruction_obj",
    [
        (
            "turn on 0,0 through 999,999",
            LightOp(turn_on, rows=range(0, 1000), cols=range(0, 1000)),
        ),
        (
            "toggle 0,0 through 123,321",
            LightOp(toggle, rows=range(0, 124), cols=range(0, 322)),
        ),
        (
            "turn off 111,0 through 0,0",
            LightOp(turn_off, rows=range(111, -1, -1), cols=range(0, -1, -1)),
        ),
        (
            "toggle 0,0 through 999,0",
            LightOp(toggle, rows=range(0, 1000), cols=range(0, 1)),
        ),
    ],
)
def test_parse_instruction(instruction_string, instruction_obj):
    assert instruction_obj == parse_instruction(instruction_string)


@pytest.mark.parametrize(
    "instructions,total_brightness",
    [
        ("\n", 0),
        ("turn on 0,0 through 0,0\n", 1),
        ("turn off 0,0 through 999,0\n", 0),
        ("turn off 499,499 through 500,500\n", 0),
        ("toggle 0,0 through 999,999\n", 2_000_000),
        (
            "turn on 0,0 through 999,999\ntoggle 499,499 through 500,500\n",
            1_000_008,
        ),
        (
            "turn on 4,4 through 8,8\n"
            "toggle 5,5 through 8,8\n"
            "turn off 5,5 through 8,8\n",
            41,
        ),
        # (aoc.get_input(2015, 6), 543903),
    ],
)
def test_configure_lights(instructions, total_brightness):
    assert total_brightness == configure_lights(instructions)
