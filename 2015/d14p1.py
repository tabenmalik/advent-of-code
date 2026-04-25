from __future__ import annotations

import re
from typing import NamedTuple

import aoc


class Reindeer(NamedTuple):
    name: str
    fly_speed: int  # km/s
    fly_duration: int  # seconds
    rest_duration: int  # seconds


RE_REINDEER = re.compile(
    r"(?P<name>\w+) can fly "
    r"(?P<fly_speed>\d+) km/s for "
    r"(?P<fly_duration>\d+) seconds, "
    "but then must rest for "
    r"(?P<rest_duration>\d+) seconds."
)


def parse_reindeer(line: str) -> Reindeer:
    m = RE_REINDEER.fullmatch(line)
    assert m is not None
    d = m.groupdict()
    name: str = d["name"]
    fly_speed = int(d["fly_speed"])
    fly_duration = int(d["fly_duration"])
    rest_duration = int(d["rest_duration"])
    return Reindeer(name, fly_speed, fly_duration, rest_duration)


def propogate_reindeer(reindeer: Reindeer, seconds: int) -> int:
    distance = 0
    while seconds != 0:
        # flying
        flying_time = min(seconds, reindeer.fly_duration)
        distance += flying_time * reindeer.fly_speed
        seconds -= flying_time
        # resting
        seconds -= min(seconds, reindeer.rest_duration)
    return distance


# default seconds given in problem statement
def race_reindeer(lines: str, seconds: int = 2503) -> int:
    reindeers = (parse_reindeer(line) for line in lines.strip().splitlines())

    return max(propogate_reindeer(reindeer, seconds) for reindeer in reindeers)


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(race_reindeer, 2015, 14),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "line,reindeer",
    [
        (
            "Comet can fly 14 km/s for 10 seconds, "
            "but then must rest for 127 seconds.",
            Reindeer("Comet", 14, 10, 127),
        ),
        (
            "Dancer can fly 16 km/s for 11 seconds, "
            "but then must rest for 162 seconds.",
            Reindeer("Dancer", 16, 11, 162),
        ),
    ],
)
def test_parse_reindeer(line, reindeer):
    assert reindeer == parse_reindeer(line)


@pytest.mark.parametrize(
    "reindeer,seconds,distance",
    [
        (Reindeer("Comet", 14, 10, 127), 1000, 1120),
        (Reindeer("Dancer", 16, 11, 162), 1000, 1056),
    ],
)
def test_propogate_reindeer(reindeer, seconds, distance):
    assert distance == propogate_reindeer(reindeer, seconds)


@pytest.mark.parametrize(
    "lines,seconds,max_distance",
    [
        (
            "Comet can fly 14 km/s for 10 seconds, "
            "but then must rest for 127 seconds.\n"
            "Dancer can fly 16 km/s for 11 seconds, "
            "but then must rest for 162 seconds.\n",
            1000,
            1120,
        ),
        (aoc.get_input(2015, 14), 2503, 2640),
    ],
)
def test_race_reindeer(lines, seconds, max_distance):
    assert max_distance == race_reindeer(lines, seconds)
