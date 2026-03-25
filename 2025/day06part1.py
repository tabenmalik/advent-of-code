from __future__ import annotations

from functools import reduce
from operator import add
from operator import mul
from typing import NamedTuple

EXAMPLE = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""


class Problem(NamedTuple):
    op: str
    numbers: tuple[int]


def _parse_problems(input_s):
    lines = input_s.strip().split("\n")
    lines = list(map(str.strip, lines))
    lines = list(map(str.split, lines))
    problem_strs = list(zip(*lines))

    problems = [
        Problem(problem_str[-1], tuple(map(int, problem_str[:-1])))
        for problem_str in problem_strs
    ]

    return problems


def _compute_problem(p: Problem):
    op = add if p.op == "+" else mul
    return reduce(op, p.numbers)


def solve(input_s):
    problems = _parse_problems(input_s)

    total_of_answers = sum(map(_compute_problem, problems))
    return total_of_answers
