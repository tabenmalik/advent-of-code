from __future__ import annotations

import argparse
from pathlib import Path
from typing import NamedTuple
from operator import add
from operator import mul
from functools import reduce


EXAMPLE = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

class Problem(NamedTuple):
    op: str
    numbers: tuple[int]


def _read_problems_correctly(p: Path) -> list[Problem]:
    with open(p) as fobj:
        worksheet = fobj.read()

    # reorient worksheet to be easier to parse
    lines = worksheet.strip("\n").split("\n")
    worksheet = "\n".join(map("".join, zip(*lines)))

    problems = []
    for problem_set in worksheet.split(f"\n{' '*len(worksheet.split('\n')[0])}\n"):
        op = problem_set.split("\n")[0][-1]
        numbers = tuple(int(line[:-1]) for line in problem_set.split("\n"))
        problems.append(Problem(op, numbers))

    return problems


def _read_problems(p: Path) -> list[Problem]:
    with open(p) as fobj:
        lines = fobj.read().strip().split("\n")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=lambda s: Path(s).absolute())
    args = parser.parse_args()

    problems = _read_problems(args.input)

    total_of_answers = sum(map(_compute_problem, problems))
    print(f"Total of answers: {total_of_answers}")

    problems = _read_problems_correctly(args.input)
    total_of_answers = sum(map(_compute_problem, problems))
    print(f"Correct total of answers: {total_of_answers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
