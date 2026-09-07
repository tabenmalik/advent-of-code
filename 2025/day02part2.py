from __future__ import annotations

from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterable
from itertools import batched
from itertools import groupby
from itertools import islice
from typing import Any


def take(n: int, iterable: Iterable[Any]) -> list[Any]:
    return list(islice(iterable, n))


def _parse_id_ranges(input_s: str) -> list[tuple[int, int]]:
    ranges = []
    for range_str in input_s.strip().split(","):
        a, _, b = range_str.partition("-")
        ranges.append((int(a), int(b)))
    return ranges


def all_equal(
    iterable: Iterable[Any],
    key: Callable[[Any], Any] | None = None,
) -> bool:
    return len(take(2, groupby(iterable, key))) <= 1


def _is_actually_invalid_id(i: int) -> bool:
    i_str = str(i)
    id_len = len(i_str)
    for split_size in range(1, id_len // 2 + 1):
        if all_equal(batched(i_str, n=split_size)):
            return True
    return False


def _get_actual_invalid_ids(id_range: tuple[int, int]) -> Generator[int]:
    for i in range(id_range[0], id_range[1] + 1):
        if _is_actually_invalid_id(i):
            yield i


def solve(input_s: str) -> int:
    id_ranges = _parse_id_ranges(input_s)
    invalid_id_sum = 0
    for id_range in id_ranges:
        invalid_id_sum += sum(_get_actual_invalid_ids(id_range))

    return invalid_id_sum
