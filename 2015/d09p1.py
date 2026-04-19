from __future__ import annotations

import re
from itertools import pairwise
from itertools import permutations

import aoc

RE_DISTANCE = re.compile(r"(\w+) to (\w+) = (\d+)")

# sparse graph representation where the key is a pair
# of locations (i.e. identifies an edge between the nodes)
# and the value is the distance between the locations
Network = dict[tuple[str, str], int]


def parse_distances(distances: str) -> Network:
    network: Network = {}

    for line in distances.strip().splitlines():
        m = RE_DISTANCE.fullmatch(line)
        assert m is not None
        network[(m.group(1), m.group(2))] = int(m.group(3))
        # add second entry to make downstream logic easier.
        # this datastructure acts like a directed graph
        # but if there's a back and forth edge then it
        # seems like an undirected graph.
        network[(m.group(2), m.group(1))] = int(m.group(3))

    return network


def distance_of_route(route: tuple[str, ...], network: Network) -> int:
    distance = 0
    for edge in pairwise(route):
        distance += network[edge]
    return distance


def find_shortest_distance(distances: str) -> int:
    network = parse_distances(distances)

    # brute force
    all_locations = {key[0] for key in network}
    all_route_distances = (
        distance_of_route(route, network) for route in permutations(all_locations)
    )
    shortest_distance = min(all_route_distances)
    return shortest_distance


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(find_shortest_distance, 2015, 9),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "distances,shortest_distance",
    [
        (
            "London to Dublin = 464\n"
            "London to Belfast = 518\n"
            "Dublin to Belfast = 141\n",
            605,
        ),
        (aoc.get_input(2015, 9), 117),
    ],
)
def test_find_shortest_distance(distances, shortest_distance):
    assert shortest_distance == find_shortest_distance(distances)
