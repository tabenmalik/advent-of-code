from __future__ import annotations

import json
from typing import Any

import aoc


def all_ints(data: Any) -> list[int]:
    if isinstance(data, int):
        return [data]
    elif isinstance(data, dict):
        ints = []
        for value in data.values():
            ints.extend(all_ints(value))
        return ints
    elif isinstance(data, list):
        ints = []
        for value in data:
            ints.extend(all_ints(value))
        return ints
    elif isinstance(data, str):
        return []

    raise NotImplementedError(f"Don't know how to process '{type(data)}' types")


def int_sum_from_json(inp: str) -> int:
    return sum(all_ints(json.loads(inp)))


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(int_sum_from_json, 2015, 12),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "inp,total",
    [
        ("{}\n", 0),
        ("[1,2,3]\n", 6),
        ('{"a":2,"b":4}\n', 6),
        ("[[[3]]]", 3),
        ('{"a":{"b":4},"c":-1}', 3),
        ('{"a":[-1,1]}', 0),
        ('[-1,{"a":1}]', 0),
        (aoc.get_input(2015, 12), 119433),
    ],
)
def test_int_sum_from_json(inp, total):
    assert total == int_sum_from_json(inp)
