from __future__ import annotations

import argparse
from itertools import batched
from itertools import chain
from itertools import groupby
from itertools import islice
from pathlib import Path
from typing import Generator
from typing import Sequence

EXAMPLE = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def take(n, iterable):
    return list(islice(iterable, n))


def all_equal(iterable, key=None):
    return len(take(2, groupby(iterable, key))) <= 1


def _is_invalid_id(i: int) -> bool:
    i_str = str(i)
    half_length = len(i_str) // 2
    return (len(i_str) % 2 == 0) and (i_str[:half_length] == i_str[half_length:])


def _is_actually_invalid_id(i: int) -> bool:
    i_str = str(i)
    l = len(i_str)
    for split_size in range(1, l // 2 + 1):
        if all_equal(batched(i_str, n=split_size)):
            return True
    return False


def _read_id_ranges(path: Path) -> tuple[tuple[int, int]]:
    with open(path) as fobj:
        range_strings = fobj.read().strip().split(",")

    ranges = [tuple(map(int, s.split("-"))) for s in range_strings]

    return ranges


def _get_invalid_ids(id_range: tuple[int, int]) -> Generator[int, None, None]:
    for i in range(id_range[0], id_range[1] + 1):
        if _is_invalid_id(i):
            yield i


def _get_actual_invalid_ids(id_range):
    for i in range(id_range[0], id_range[1] + 1):
        if _is_actually_invalid_id(i):
            yield i


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=lambda s: Path(s).absolute())
    args = parser.parse_args(argv)

    id_ranges = _read_id_ranges(args.input)
    invalid_id_sum = 0
    for id_range in id_ranges:
        invalid_id_sum += sum(_get_invalid_ids(id_range))

    print(f"Sum of invalid ids: {invalid_id_sum}")

    invalid_id_sum = 0
    for id_range in id_ranges:
        invalid_id_sum += sum(_get_actual_invalid_ids(id_range))

    print(f"Sum of actual invalid ids: {invalid_id_sum}")


if __name__ == "__main__":
    raise SystemExit(_main())
