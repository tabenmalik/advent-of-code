from __future__ import annotations

from itertools import batched
from itertools import groupby
from itertools import islice


def take(n, iterable):
    return list(islice(iterable, n))


def _parse_id_ranges(input_s):
    input_s = input_s.strip().split(",")
    ranges = [tuple(map(int, s.split("-"))) for s in input_s]
    return ranges


def all_equal(iterable, key=None):
    return len(take(2, groupby(iterable, key))) <= 1


def _is_actually_invalid_id(i: int) -> bool:
    i_str = str(i)
    id_len = len(i_str)
    for split_size in range(1, id_len // 2 + 1):
        if all_equal(batched(i_str, n=split_size)):
            return True
    return False


def _get_actual_invalid_ids(id_range):
    for i in range(id_range[0], id_range[1] + 1):
        if _is_actually_invalid_id(i):
            yield i


def solve(input_s):
    id_ranges = _parse_id_ranges(input_s)
    invalid_id_sum = 0
    for id_range in id_ranges:
        invalid_id_sum += sum(_get_actual_invalid_ids(id_range))

    return invalid_id_sum
