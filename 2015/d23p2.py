from __future__ import annotations

from typing import NamedTuple

import aoc

ProgramCounter = int


class Registers(NamedTuple):
    a: int
    b: int


def hlf(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    return regs._replace(**{arg: getattr(regs, arg) // 2}), pc + 1


def tpl(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    return regs._replace(**{arg: getattr(regs, arg) * 3}), pc + 1


def inc(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    return regs._replace(**{arg: getattr(regs, arg) + 1}), pc + 1


def jmp(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    return regs, pc + int(arg)


def jie(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    reg, offset = arg.split(", ")
    if getattr(regs, reg) % 2 == 0:
        return regs, pc + int(offset)
    else:
        return regs, pc + 1


def jio(
    arg: str, regs: Registers, pc: ProgramCounter,
) -> tuple[Registers, ProgramCounter]:
    reg, offset = arg.split(", ")
    if getattr(regs, reg) == 1:
        return regs, pc + int(offset)
    else:
        return regs, pc + 1


def run(instrs: tuple[str, ...]) -> Registers:
    regs: Registers = Registers(a=1, b=0)
    pc: int = 0

    while True:
        if pc >= len(instrs):
            break

        cmd, _, args = instrs[pc].partition(" ")

        if cmd == "hlf":
            regs, pc = hlf(args, regs, pc)
        elif cmd == "tpl":
            regs, pc = tpl(args, regs, pc)
        elif cmd == "inc":
            regs, pc = inc(args, regs, pc)
        elif cmd == "jmp":
            regs, pc = jmp(args, regs, pc)
        elif cmd == "jie":
            regs, pc = jie(args, regs, pc)
        elif cmd == "jio":
            regs, pc = jio(args, regs, pc)

    return regs


def solve(inp: str) -> int:
    instrs = tuple(inp.strip().splitlines())
    regs = run(instrs)
    return regs.b


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 23),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 23), 231)])
def test_solve(inp, result):
    assert result == solve(inp)
