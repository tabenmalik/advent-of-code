from __future__ import annotations

from aoc.year2025.day06part1 import Problem
from aoc.year2025.day06part1 import _compute_problem


def _parse_problems_correctly(input_s):
    worksheet = input_s

    # reorient worksheet to be easier to parse
    lines = worksheet.strip("\n").split("\n")
    worksheet = "\n".join(map("".join, zip(*lines)))

    problems = []
    for problem_set in worksheet.split(f"\n{' '*len(worksheet.split('\n')[0])}\n"):
        op = problem_set.split("\n")[0][-1]
        numbers = tuple(int(line[:-1]) for line in problem_set.split("\n"))
        problems.append(Problem(op, numbers))

    return problems


def solve(input_s):
    problems = _parse_problems_correctly(input_s)
    total_of_answers = sum(map(_compute_problem, problems))
    return total_of_answers
