from __future__ import annotations

from collections import Counter

EXAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def _parse_rotations(s: str) -> tuple[int, ...]:
    rot_strs = [rot.replace("R", "").replace("L", "-") for rot in s.strip().split()]
    return tuple(map(int, rot_strs))


def _safe_password(dial_start: int, rotations: tuple[int]) -> int:
    # the password is the number of times the dial
    # left pointing at 0 after any rotation in the sequence
    dial_value = dial_start
    dial_values = [dial_value := (dial_value + rot) % 100 for rot in rotations]
    return Counter(dial_values)[0]


def solve(input_s):
    rotations = _parse_rotations(input_s)
    password = _safe_password(50, rotations)

    return password
