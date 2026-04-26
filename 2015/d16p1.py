from __future__ import annotations

import re

import aoc

SueProp = tuple[str, int]
Sue = set[SueProp]


def parse_sues(sue_doc: str) -> dict[int, Sue]:
    sues: dict[int, Sue] = {}
    re_prop = re.compile(r"(\w+): (\d+)")
    for i, line in enumerate(sue_doc.strip().splitlines(), 1):
        props = {(prop[0], int(prop[1])) for prop in re_prop.findall(line)}
        sues[i] = props
    return sues


def determine_sue(sue_doc: str) -> int:
    mfcsam_result = {
        ("children", 3),
        ("cats", 7),
        ("samoyeds", 2),
        ("pomeranians", 3),
        ("akitas", 0),
        ("vizslas", 0),
        ("goldfish", 5),
        ("trees", 3),
        ("cars", 2),
        ("perfumes", 1),
    }

    sues = parse_sues(sue_doc)

    for sue, sue_props in sues.items():
        if sue_props.issubset(mfcsam_result):
            return sue
    raise AssertionError


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(determine_sue, 2015, 16),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 16), 40)])
def test_determine_sue(inp, result):
    assert result == determine_sue(inp)
