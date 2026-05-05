from __future__ import annotations

from collections.abc import Iterator
from itertools import combinations
from itertools import product
from typing import NamedTuple

import aoc


class Item(NamedTuple):
    cost: int
    damage: int
    armor: int


SHOP = {
    "Weapons": [
        Item(cost=8, damage=4, armor=0),  # Dagger
        Item(cost=10, damage=5, armor=0),  # Shortsword
        Item(cost=25, damage=6, armor=0),  # Warhammer
        Item(cost=40, damage=7, armor=0),  # Longsword
        Item(cost=74, damage=8, armor=0),  # Greataxe
    ],
    "Armor": [
        Item(cost=0, damage=0, armor=0),  # equivalent to no armor
        Item(cost=13, damage=0, armor=1),  # Leather
        Item(cost=31, damage=0, armor=2),  # Chainmail
        Item(cost=53, damage=0, armor=3),  # Splintmail
        Item(cost=75, damage=0, armor=4),  # Bandedmail
        Item(cost=102, damage=0, armor=5),  # Platemail
    ],
    "Rings": [
        # 2 empty rings since player could chose 0-2 rings
        Item(cost=0, damage=0, armor=0),  # equivalent to no ring
        Item(cost=0, damage=0, armor=0),  # equivalent to no ring
        Item(cost=25, damage=1, armor=0),  # Damage +1
        Item(cost=50, damage=2, armor=0),  # Damage +1
        Item(cost=100, damage=3, armor=0),  # Damage +1
        Item(cost=20, damage=0, armor=1),  # Damage +1
        Item(cost=40, damage=0, armor=2),  # Damage +1
        Item(cost=80, damage=0, armor=3),  # Damage +1
    ],
}


class Player(NamedTuple):
    hp: int
    damage: int
    armor: int

    @classmethod
    def from_input(cls, lines: str) -> Player:
        hit_points, damage, armor = lines.strip().splitlines()
        return cls(
            hp=int(hit_points.split(":")[1]),
            damage=int(damage.split(":")[1]),
            armor=int(armor.split(":")[1]),
        )


def all_player_builds(player_hp: int = 100) -> Iterator[tuple[Player, int]]:
    """Yield all player builds and their cost."""
    weapons = SHOP["Weapons"]
    armors = SHOP["Armor"]
    all_rings = list(combinations(SHOP["Rings"], 2))
    for weapon, armor, rings in product(weapons, armors, all_rings):
        player = Player(
            hp=player_hp,
            damage=weapon.damage + sum(ring.damage for ring in rings),
            armor=armor.armor + sum(ring.armor for ring in rings),
        )
        cost = weapon.cost + armor.cost + sum(ring.cost for ring in rings)

        yield player, cost


def battle(player: Player, boss: Player) -> bool:
    """Return True if `player` beats `boss`"""
    player_hp = player.hp
    boss_hp = boss.hp

    while True:
        # player always starts first
        boss_hp -= max(1, player.damage - boss.armor)
        if boss_hp <= 0:
            return True

        player_hp -= max(1, boss.damage - player.armor)
        if player_hp <= 0:
            return False


def solve(inp: str, player_hp: int = 100) -> int:
    boss = Player.from_input(inp)

    max_cost = 0
    for player, cost in all_player_builds(player_hp):
        # only check builds that could potentially increase the cost
        if cost > max_cost and not battle(player, boss):
            max_cost = cost
    return max_cost


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 21),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "player, boss, player_wins",
    [
        # player deals damage below 0
        (Player(hp=8, damage=5, armor=5), Player(hp=12, damage=7, armor=2), True),
        # player deals damage to exactly 0
        (Player(hp=8, damage=12, armor=5), Player(hp=12, damage=7, armor=0), True),
        # boss deals damage to below 0
        (Player(hp=8, damage=1, armor=0), Player(hp=12, damage=9, armor=2), False),
        # boss deals damage to exactly 0
        (Player(hp=8, damage=1, armor=0), Player(hp=12, damage=8, armor=2), False),
    ],
)
def test_battle(player, boss, player_wins):
    assert player_wins == battle(player, boss)


def test_player_builds():
    assert 840 == len(list(all_player_builds()))


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 21), 188)])
def test_solve(inp, result):
    assert result == solve(inp)
