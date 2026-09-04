from __future__ import annotations

from functools import reduce
from operator import add
from operator import mul
from typing import NamedTuple


def _compute_problem(p: Problem) -> int:
    op = add if p.op == "+" else mul
    return reduce(op, p.numbers)


class Problem(NamedTuple):
    op: str
    numbers: tuple[int, ...]


def _parse_problems_correctly(input_s: str) -> list[Problem]:
    worksheet = input_s

    # reorient worksheet to be easier to parse
    lines = worksheet.strip("\n").split("\n")
    worksheet = "\n".join(map("".join, zip(*lines)))

    problems = []
    first = worksheet.split('\n')[0]
    for problem_set in worksheet.split(f"\n{' '*len(first)}\n"):
        op = problem_set.split("\n")[0][-1]
        numbers = tuple(int(line[:-1]) for line in problem_set.split("\n"))
        problems.append(Problem(op, numbers))

    return problems


def solve(input_s: str) -> int:
    problems = _parse_problems_correctly(input_s)
    total_of_answers = sum(map(_compute_problem, problems))
    return total_of_answers
