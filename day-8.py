from __future__ import annotations

import argparse
from pathlib import Path
from math import sqrt
from typing import NamedTuple
from itertools import combinations
from functools import cached_property
from functools import cache
from functools import reduce
from operator import mul

class Junction(NamedTuple):
    x: int
    y: int
    z: int


class JunctionGraph:

    def __init__(self, junctions):
        # keys are nodes, values are connections to other nodes
        self._graph = {j: set() for j in junctions}
        self._shortest_distances = [(j1, j2) for j1, j2 in combinations(junctions, 2)]
        self._shortest_distances.sort(key=lambda pair: distance(*pair))
        self._connection_cache = set()

    def connect(self, j1, j2):
        print(j1, j2)
        self._graph[j1].add(j2)
        self._graph[j2].add(j1)

        checked = set()
        connected = {j1}
        while connected:
            junction = connected.pop()
            checked.add(junction)
            self._connection_cache.add(tuple(sorted([junction, j1])))
            self._connection_cache.add(tuple(sorted([junction, j2])))
            for connection in self._graph[junction]:
                if connection not in checked:
                    connected.add(connection)

    def are_connected(self, j1, j2, *, checked=None):
        j1, j2 = sorted([j1, j2])
        if (j1, j2) in self._connection_cache:
            return True
        return False

        #checked = set()
        #to_check = {j1}
        #while to_check:
        #    junction = to_check.pop()
        #    if junction == j2:
        #        self._connection_cache.add((j1, j2))
        #        return True
        #    checked.add(junction)
        #    for connection in self._graph[junction]:
        #        if connection not in checked:
        #            to_check.add(connection)
        #return False

    @cached_property
    def max_distance(self):
        max_dist = 0
        for (j1, j2) in combinations(self._graph, 2):
            max_dist = max(max_dist, distance(j1, j2))

        return max_dist


    def closest_non_connected_junctions(self, max_pairs):
        for i, pair in enumerate(self._shortest_distances):
            if i >= max_pairs:
                break
            if not self.are_connected(*pair):
                return pair
        return None

    def circuits(self):
        cs = []
        for junction in self._graph:
            for circuit in cs:
                if self.are_connected(junction, next(iter(circuit))):
                    circuit.add(junction)
                    break
            else:
                cs.append({junction})
        return cs


@cache
def distance(j1, j2):
    return sqrt((j2.x - j1.x) ** 2 + (j2.y - j1.y) ** 2 + (j2.z - j1.z) ** 2)


def _read_junction_locations(p):
    with open(p) as fobj:
        point_strs = fobj.read().strip().split()

    junctions = tuple(
        Junction(*map(int, point_str.split(",")))
        for point_str in point_strs
    )

    return JunctionGraph(junctions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", type=int)
    parser.add_argument("input", type=lambda s: Path(s).absolute())
    args = parser.parse_args()

    junction_graph = _read_junction_locations(args.input)
    while (junction_pair := junction_graph.closest_non_connected_junctions(args.pairs)) is not None:
        junction_graph.connect(*junction_pair)
    circuits = junction_graph.circuits()
    circuits.sort(key=len, reverse=True)
    circuit_multiply = reduce(mul, map(len, circuits[:3]), 1)
    print(f"Multiplication of three largest circuits: {circuit_multiply}")

    last_junction_pair = None
    while (junction_pair := junction_graph.closest_non_connected_junctions(1_000_000_000)) is not None:
        junction_graph.connect(*junction_pair)
        last_junction_pair = junction_pair
    print(f"Coordinate multiply of last connected junction: {last_junction_pair[0].x * last_junction_pair[1].x}")

if __name__ == "__main__":
    raise SystemExit(main())
