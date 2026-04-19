from __future__ import annotations

import operator
import re
from collections.abc import Callable
from typing import NamedTuple

import aoc

WireGraph = dict[str, int]


def op_const(val: int) -> int:
    return val


def op_not(val: int) -> int:
    return val ^ 65535


def find_values(
    sources: tuple[str, ...], wire_graph: WireGraph
) -> tuple[int, ...] | None:
    values: list[int] = []
    for source in sources:
        if source.isalpha():
            if source not in wire_graph:
                return None
            values.append(wire_graph[source])
        else:
            values.append(int(source))
    return tuple(values)


class LogicGate(NamedTuple):
    dest: str
    sources: tuple[str, ...]
    op: Callable


RE_AND = re.compile(r"(\w+) AND (\w+) -> (\w+)")

RE_CONST = re.compile(r"(\w+) -> (\w+)")

RE_LSHIFT = re.compile(r"(\w+) LSHIFT (\w+) -> (\w+)")

RE_RSHIFT = re.compile(r"(\w+) RSHIFT (\w+) -> (\w+)")

RE_NOT = re.compile(r"NOT (\w+) -> (\w+)")

RE_OR = re.compile(r"(\w+) OR (\w+) -> (\w+)")


def parse_logic_gate(line: str) -> LogicGate:
    if m := RE_AND.fullmatch(line):
        return LogicGate(m.group(3), (m.group(1), m.group(2)), operator.and_)
    elif m := RE_CONST.fullmatch(line):
        return LogicGate(m.group(2), (m.group(1),), op_const)
    elif m := RE_LSHIFT.fullmatch(line):
        return LogicGate(m.group(3), (m.group(1), m.group(2)), operator.lshift)
    elif m := RE_RSHIFT.fullmatch(line):
        return LogicGate(m.group(3), (m.group(1), m.group(2)), operator.rshift)
    elif m := RE_NOT.fullmatch(line):
        return LogicGate(m.group(2), (m.group(1),), op_not)
    elif m := RE_OR.fullmatch(line):
        return LogicGate(m.group(3), (m.group(1), m.group(2)), operator.or_)

    raise NotImplementedError(f"{line}")


def solve(inp: str) -> str:
    wire_graph: WireGraph = {}
    logic_gates = tuple(parse_logic_gate(line) for line in inp.strip().splitlines())

    while "a" not in wire_graph:
        for logic_gate in logic_gates:
            values = find_values(logic_gate.sources, wire_graph)
            if values is None:
                continue
            wire_graph[logic_gate.dest] = logic_gate.op(*values)

    # part 2 extension
    a = wire_graph["a"]
    wire_graph = {}
    wire_graph["b"] = a

    while "a" not in wire_graph:
        for logic_gate in logic_gates:
            if logic_gate.dest in wire_graph:
                continue
            values = find_values(logic_gate.sources, wire_graph)
            if values is None:
                continue
            wire_graph[logic_gate.dest] = logic_gate.op(*values)

    return str(wire_graph["a"])


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 7),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "line,logic_gate",
    [
        ("2 AND 2 -> x", LogicGate("x", ("2", "2"), operator.and_)),
        ("yy -> a", LogicGate("a", ("yy",), op_const)),
        ("42 -> ab", LogicGate("ab", ("42",), op_const)),
        ("5 LSHIFT et -> ui", LogicGate("ui", ("5", "et"), operator.lshift)),
        ("v RSHIFT 67 -> l", LogicGate("l", ("v", "67"), operator.rshift)),
        ("NOT ii -> gg", LogicGate("gg", ("ii",), op_not)),
        ("NOT 5 -> w", LogicGate("w", ("5",), op_not)),
        ("34 OR cd -> y", LogicGate("y", ("34", "cd"), operator.or_)),
    ],
)
def test_parse_logic_gate(line, logic_gate):
    assert logic_gate == parse_logic_gate(line)


@pytest.mark.parametrize(
    "logic_lines,value_of_a",
    [
        ("2 -> x\nNOT x -> a", "65533"),
        ("2 -> b\nb LSHIFT 1 -> a", "8"),
        (aoc.get_input(2015, 7), "2797"),
    ],
)
def test_solve(logic_lines, value_of_a):
    assert value_of_a == solve(logic_lines)
