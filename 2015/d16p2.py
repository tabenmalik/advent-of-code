from __future__ import annotations

import re

import aoc

Sue = dict[str, int]


def parse_sues(sue_doc: str) -> dict[int, Sue]:
    sues: dict[int, Sue] = {}
    re_prop = re.compile(r"(\w+): (\d+)")
    for i, line in enumerate(sue_doc.strip().splitlines(), 1):
        props = {(prop[0], int(prop[1])) for prop in re_prop.findall(line)}
        sues[i] = dict(props)
    return sues


def determine_sue(sue_doc: str) -> int:
    mfcsam_result = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    sues = parse_sues(sue_doc)

    for sue_num, sue in sues.items():
        if "cats" in sue and sue["cats"] <= mfcsam_result["cats"]:
            continue

        if "trees" in sue and sue["trees"] <= mfcsam_result["trees"]:
            continue

        if "pomeranians" in sue and sue["pomeranians"] >= mfcsam_result["pomeranians"]:
            continue

        if "goldfish" in sue and sue["goldfish"] >= mfcsam_result["goldfish"]:
            continue

        # remaining sue properties must be exact
        sue_props = {
            prop
            for prop in sue.items()
            if prop[0] not in {"cats", "trees", "pomeranians", "goldfish"}
        }
        if sue_props.issubset(set(mfcsam_result.items())):
            return sue_num
    raise AssertionError


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(determine_sue, 2015, 16),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 16), 241)])
def test_determine_sue(inp, result):
    assert result == determine_sue(inp)
