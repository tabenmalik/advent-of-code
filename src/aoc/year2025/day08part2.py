from __future__ import annotations

from itertools import product
from math import sqrt
from pprint import pprint
from time import sleep
from typing import NamedTuple

EXAMPLE = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


class Junction(NamedTuple):

    x: int
    y: int
    z: int

    @classmethod
    def from_csv(cls, s):
        return cls(*map(int, s.strip().split(",")))

    def distance(self, j):
        return sqrt((j.x - self.x) ** 2 + (j.y - self.y) ** 2 + (j.z - self.z) ** 2)


def _condense_circuits(junction_graph):
    new_junction_graph = []
    new_junction_graph.append(junction_graph[0])

    for circuit in junction_graph:
        for new_circuit in new_junction_graph:
            if circuit.intersection(new_circuit):
                new_circuit.update(circuit)
                break
        else:
            new_junction_graph.append(circuit)
    return new_junction_graph


def _last_connected_junctions(junctions):
    junction_graph: list[set[Junction]] = []

    junction_pairs = product(junctions, junctions)
    junction_pairs = sorted(junction_pairs, key=lambda p: p[0].distance(p[1]))
    for j1, j2 in junction_pairs:
        if j1 == j2:
            continue

        for circuit in junction_graph:
            if j1 in circuit or j2 in circuit:
                circuit.update((j1, j2))
                junction_graph = _condense_circuits(junction_graph)
                break
        else:
            junction_graph.append({j1, j2})

        if len(junction_graph) == 1 and len(junction_graph[0]) == len(junctions):
            break

    return j1, j2


def _read_input(input_s) -> tuple[Junction]:
    return tuple(map(Junction.from_csv, input_s.strip().split("\n")))


def solve(input_s):
    junctions = _read_input(input_s)
    j1, j2 = _last_connected_junctions(junctions)
    return j1.x * j2.x
