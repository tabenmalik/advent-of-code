from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from math import copysign
from itertools import repeat

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


def _read_rotations(path: Path) -> tuple[int]:
    with open(path) as fobj:
        rot_strs = fobj.read().split()

    rot_strs = [rot.replace("R", "").replace("L", "-") for rot in rot_strs]
    return tuple(map(int, rot_strs))


def _safe_password(dial_start: int, rotations: tuple[int]) -> int:
    # the password is the number of times the dial
    # left pointing at 0 after any rotation in the sequence
    dial_value = dial_start
    dial_values = [dial_value := (dial_value + rot) % 100 for rot in rotations]
    return Counter(dial_values)[0]


def _safe_password_434C49434B(dial_start: int, rotations: tuple[int]) -> int:
    # actually... the real password the number of times any clock
    # causes the dial to point at 0, including crossing 0 in a rotation
    dial_value = dial_start
    zero_count = 0
    for rotation in rotations:
        step = copysign(1, rotation)
        for step in repeat(step, abs(rotation)):
            dial_value = (dial_value + step) % 100
            if dial_value == 0:
                zero_count += 1

    return zero_count


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dial-start", type=int, default=50)
    parser.add_argument("input", type=lambda s: Path(s).absolute())
    args = parser.parse_args(argv)

    rotations = _read_rotations(args.input)

    password = _safe_password(args.dial_start, rotations)
    print(f"Safe password: {password}")

    password = _safe_password_434C49434B(args.dial_start, rotations)
    print(f"jk the real safe password: {password}")


if __name__ == "__main__":
    raise SystemExit(_main())
