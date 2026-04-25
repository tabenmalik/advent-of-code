from __future__ import annotations

import re
from dataclasses import dataclass
from typing import NamedTuple

import aoc


class Reindeer(NamedTuple):
    name: str
    fly_speed: int  # km/s
    fly_duration: int  # seconds
    rest_duration: int  # seconds


@dataclass
class ReindeerRaceState:
    reindeer: Reindeer
    countdown: int
    flying: bool = True
    distance: int = 0
    points: int = 0

    def tick(self):
        if self.flying:
            self.distance += self.reindeer.fly_speed
        self.countdown -= 1

        if self.countdown == 0:
            if self.flying:
                self.countdown = self.reindeer.rest_duration
            else:
                self.countdown = self.reindeer.fly_duration
            self.flying = not self.flying

    def give_point(self):
        self.points += 1


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


def propogate_reindeers(
    reindeer_race: tuple[ReindeerRaceState, ...],
):
    for reindeer in reindeer_race:
        reindeer.tick()

    lead_reindeers = [reindeer_race[0]]
    for reindeer in reindeer_race[1:]:
        if reindeer.distance == lead_reindeers[0].distance:
            lead_reindeers.append(reindeer)
        elif reindeer.distance > lead_reindeers[0].distance:
            lead_reindeers = [reindeer]

    for reindeer in lead_reindeers:
        reindeer.give_point()


# default seconds given in problem statement
def race_reindeer(lines: str, seconds: int = 2503) -> int:
    reindeers = tuple(parse_reindeer(line) for line in lines.strip().splitlines())

    reindeer_race = tuple(
        ReindeerRaceState(reindeer, reindeer.fly_duration) for reindeer in reindeers
    )

    for _ in range(seconds):
        propogate_reindeers(reindeer_race)

    return max(reindeer.points for reindeer in reindeer_race)


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
    "lines,seconds,max_distance",
    [
        (
            "Comet can fly 14 km/s for 10 seconds, "
            "but then must rest for 127 seconds.\n"
            "Dancer can fly 16 km/s for 11 seconds, "
            "but then must rest for 162 seconds.\n",
            1000,
            689,
        ),
        (aoc.get_input(2015, 14), 2503, 1102),
    ],
)
def test_race_reindeer(lines, seconds, max_distance):
    assert max_distance == race_reindeer(lines, seconds)
