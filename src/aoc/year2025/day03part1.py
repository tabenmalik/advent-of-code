from __future__ import annotations

import argparse
from collections.abc import Sequence
from itertools import combinations
from pathlib import Path

EXAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""


def _max_joltage_batteries(bank: str, num_batteries: int):
    joltage_index = 0
    for joltage in range(9, 0, -1):
        joltage_index = bank.find(str(joltage), 0, len(bank) - num_batteries + 1)
        if joltage_index != -1:
            break

    if num_batteries == 1:
        return bank[joltage_index]
    return bank[joltage_index] + _max_joltage_batteries(
        bank[joltage_index + 1 :], num_batteries - 1
    )


def _max_joltage(bank: str, num_batteries: int) -> int:
    return int(_max_joltage_batteries(bank, num_batteries))


def _total_max_joltage(banks, num_batteries):
    return sum(map(lambda bank: _max_joltage(bank, num_batteries), banks))


def _read_battery_banks(path: Path):
    with open(path) as fobj:
        return fobj.read().strip().split()


def _parse_battery_banks(input_s):
    return input_s.strip().split()


def solve(input_s, num_batteries=2):
    banks = _parse_battery_banks(input_s)
    joltage = _total_max_joltage(banks, num_batteries)
    return joltage
