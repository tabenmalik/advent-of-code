from __future__ import annotations

import json
from typing import Any

import aoc


def all_ints_except_red(data: Any) -> list[int]:
    if isinstance(data, int):
        return [data]
    elif isinstance(data, dict):
        if "red" in list(data.values()):
            return []
        ints = []
        for value in data.values():
            ints.extend(all_ints_except_red(value))
        return ints
    elif isinstance(data, list):
        ints = []
        for value in data:
            ints.extend(all_ints_except_red(value))
        return ints
    elif isinstance(data, str):
        return []

    raise NotImplementedError(f"Don't know how to process '{type(data)}' types")


def int_sum_from_json(inp: str) -> int:
    return sum(all_ints_except_red(json.loads(inp)))


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
        ('[1,{"c":"red","b":2},3]', 4),
        ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
        ('[1,"red",5]', 6),
        (aoc.get_input(2015, 12), 68466),
    ],
)
def test_int_sum_from_json(inp, total):
    assert total == int_sum_from_json(inp)
