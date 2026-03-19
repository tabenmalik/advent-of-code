from __future__ import annotations

from itertools import repeat
from math import copysign


def _parse_rotations(s: str) -> tuple[int, ...]:
    rot_strs = [rot.replace("R", "").replace("L", "-") for rot in s.strip().split()]
    return tuple(map(int, rot_strs))


def _safe_password(dial_start: int, rotations: tuple[int, ...]) -> int:
    # actually... the real password the number of times any clock
    # causes the dial to point at 0, including crossing 0 in a rotation
    dial_value = dial_start
    zero_count = 0
    for rotation in rotations:
        step = copysign(1, rotation)
        for step in repeat(step, abs(rotation)):
            dial_value = int((dial_value + step) % 100)
            if dial_value == 0:
                zero_count += 1

    return zero_count


def solve(input_s):
    rotations = _parse_rotations(input_s)
    password = _safe_password(50, rotations)
    return password
