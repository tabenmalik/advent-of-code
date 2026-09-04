from __future__ import annotations


def _ranges_overlap(a: range, b: range) -> bool:
    return a.start < b.stop and a.stop > b.start


def _parse_ingredient_database(input_s: str) -> tuple[list[range], list[int]]:
    id_range_strs = []
    file_iter = iter(input_s.split("\n"))
    for line in file_iter:
        if not line.strip():
            break
        id_range_strs.append(line)

    id_strs = []
    for line in file_iter:
        if line.strip():
            id_strs.append(line)

    id_ranges = [
        range(*map(int, id_range_str.split("-")))
        for id_range_str in id_range_strs
    ]

    ids = list(map(int, id_strs))

    return id_ranges, ids


def _merge_id_ranges(id_ranges: list[range]) -> list[range]:
    id_ranges = sorted(id_ranges, key=lambda x: x[0])
    merged_id_ranges = [id_ranges[0]]
    for id_range in id_ranges[1:]:
        if _ranges_overlap(merged_id_ranges[-1], id_range):
            merged_id_ranges[-1] = range(
                merged_id_ranges[-1][0],
                max(merged_id_ranges[-1][1], id_range[1]),
            )
        else:
            merged_id_ranges.append(id_range)

    return merged_id_ranges


def _num_of_available_fresh_ids(id_ranges: list[range]) -> int:
    total = 0
    for id_range in id_ranges:
        total += len(id_range) + 1
    return total


def solve(input_s: str) -> int:
    id_ranges, ids = _parse_ingredient_database(input_s)
    id_ranges = _merge_id_ranges(id_ranges)
    available_fresh_ids = _num_of_available_fresh_ids(id_ranges)
    return available_fresh_ids
