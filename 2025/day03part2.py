from __future__ import annotations

from pathlib import Path


def _max_joltage_batteries(bank: str, num_batteries: int) -> str:
    joltage_index = 0
    for joltage in range(9, 0, -1):
        joltage_index = bank.find(
            str(joltage), 0, len(bank) - num_batteries + 1,
        )
        if joltage_index != -1:
            break

    if num_batteries == 1:
        return bank[joltage_index]
    return bank[joltage_index] + _max_joltage_batteries(
        bank[joltage_index + 1:], num_batteries - 1,
    )


def _max_joltage(bank: str, num_batteries: int) -> int:
    return int(_max_joltage_batteries(bank, num_batteries))


def _total_max_joltage(banks: list[str], num_batteries: int) -> int:
    return sum(map(lambda bank: _max_joltage(bank, num_batteries), banks))


def _read_battery_banks(path: Path) -> list[str]:
    with open(path) as fobj:
        return fobj.read().strip().split()


def _parse_battery_banks(input_s: str) -> list[str]:
    return input_s.strip().split()


def solve(input_s: str, num_batteries: int = 12) -> int:
    banks = _parse_battery_banks(input_s)
    joltage = _total_max_joltage(banks, num_batteries)
    return joltage
