from __future__ import annotations

import heapq
from typing import NamedTuple

import aoc

MAGIC_MISSILE_COST = 53
MAGIC_MISSILE_DAMAGE = 4

DRAIN_COST = 73
DRAIN_DAMAGE = 2
DRAIN_HEAL = 2

SHIELD_COST = 113
SHIELD_ARMOR = 7
SHIELD_TURNS = 6

POISON_COST = 173
POISON_TURNS = 6
POISON_DAMAGE = 3

RECHARGE_COST = 229
RECHARGE_TURNS = 5
RECHARGE_MANA = 101


class Player(NamedTuple):
    hp: int
    armor: int
    mana: int
    damage: int = 0


def sub_mana(player: Player, mana: int) -> Player:
    assert mana <= player.mana
    return player._replace(mana=player.mana - mana)


def heal(player: Player, hp: int) -> Player:
    return player._replace(hp=player.hp + hp)


def attack(attacker: Player, attacked: Player, bonus_damage: int = 0) -> Player:
    hp = attacked.hp + attacked.armor - attacker.damage - bonus_damage
    hp = max(0, hp)
    return attacked._replace(hp=hp)


class GameState(NamedTuple):
    player: Player
    boss: Player

    # counters for each effect
    shield: int = 0
    poison: int = 0
    recharge: int = 0

    # total_mana, __lt__, and __eq__ will be used to sort
    # game states for finding optimal play strategy
    total_mana: int = 0

    def __lt__(self, other: object):
        if not isinstance(other, GameState):
            return NotImplemented
        else:
            return self.total_mana < other.total_mana

    def __eq__(self, other: object):
        if not isinstance(other, GameState):
            return NotImplemented
        else:
            return self.total_mana == other.total_mana


def game_over(game: GameState) -> bool:
    return (
        game.player.hp == 0
        or game.player.mana < MAGIC_MISSILE_COST
        or game.boss.hp == 0
    )


def available_moves(game: GameState) -> tuple[str, ...]:
    moves = []

    if game.player.mana >= MAGIC_MISSILE_COST:
        moves.append("Magic Missile")

    if game.player.mana >= DRAIN_COST:
        moves.append("Drain")

    # effects can be started on the same turn
    # they end i.e. when effect counters are 1
    if game.shield <= 1 and game.player.mana >= SHIELD_COST:
        moves.append("Shield")

    if game.poison <= 1 and game.player.mana >= POISON_COST:
        moves.append("Poison")

    if game.recharge <= 1 and game.player.mana >= RECHARGE_COST:
        moves.append("Recharge")

    return tuple(moves)


def magic_missile(game: GameState) -> GameState:
    new_total_mana = game.total_mana + MAGIC_MISSILE_COST
    player = sub_mana(game.player, MAGIC_MISSILE_COST)
    boss = attack(game.player, game.boss, MAGIC_MISSILE_DAMAGE)
    game = game._replace(boss=boss, player=player, total_mana=new_total_mana)
    return game


def drain(game: GameState) -> GameState:
    new_total_mana = game.total_mana + DRAIN_COST
    player = sub_mana(game.player, DRAIN_COST)
    boss = attack(game.player, game.boss, DRAIN_DAMAGE)
    player = heal(player, DRAIN_HEAL)
    game = game._replace(boss=boss, player=player, total_mana=new_total_mana)
    return game


def shield(game: GameState) -> GameState:
    assert game.shield == 0

    new_total_mana = game.total_mana + SHIELD_COST
    player = sub_mana(game.player, SHIELD_COST)
    player = player._replace(armor=SHIELD_ARMOR)
    game = game._replace(
        player=player, total_mana=new_total_mana, shield=SHIELD_TURNS,
    )
    return game


def poison(game: GameState) -> GameState:
    assert game.poison == 0
    new_total_mana = game.total_mana + POISON_COST
    player = sub_mana(game.player, POISON_COST)
    game = game._replace(
        player=player, total_mana=new_total_mana, poison=POISON_TURNS,
    )
    return game


def recharge(game: GameState) -> GameState:
    assert game.recharge == 0
    new_total_mana = game.total_mana + RECHARGE_COST
    player = sub_mana(game.player, RECHARGE_COST)
    game = game._replace(
        player=player, total_mana=new_total_mana, recharge=RECHARGE_TURNS,
    )
    return game


def effects(game: GameState) -> GameState:

    if game.poison > 0:
        new_poison = game.poison - 1
        new_boss_hp = max(0, game.boss.hp - POISON_DAMAGE)
        new_boss = game.boss._replace(hp=new_boss_hp)
        game = game._replace(boss=new_boss, poison=new_poison)

    if game.recharge > 0:
        new_recharge = game.recharge - 1
        new_player_mana = game.player.mana + RECHARGE_MANA
        new_player = game.player._replace(mana=new_player_mana)
        game = game._replace(player=new_player, recharge=new_recharge)

    if game.shield > 0:
        new_shield = game.shield - 1
        game = game._replace(shield=new_shield)
        if new_shield == 0:
            new_player = game.player._replace(armor=0)
            game = game._replace(player=new_player)

    return game


def boss_attack(game: GameState) -> GameState:
    new_player_hp = max(
        0, game.player.hp -
        game.boss.damage + game.player.armor,
    )
    new_player = game.player._replace(hp=new_player_hp)
    game = game._replace(player=new_player)
    return game


def player_damage(game: GameState) -> GameState:
    player = game.player._replace(hp=game.player.hp - 1)
    return game._replace(player=player)


def progress(game: GameState, move: str) -> GameState:
    assert move in available_moves(game)

    game = effects(game)
    if game.boss.hp == 0:
        return game

    if move == "Magic Missile":
        game = magic_missile(game)
    elif move == "Drain":
        game = drain(game)
    elif move == "Shield":
        game = shield(game)
    elif move == "Poison":
        game = poison(game)
    elif move == "Recharge":
        game = recharge(game)

    if game.boss.hp == 0:
        return game

    game = effects(game)
    if game.boss.hp == 0:
        return game
    game = boss_attack(game)

    return game


def solve(inp: str) -> int:
    player = Player(50, 0, 500, 0)
    hp_line, damage_line = inp.strip().splitlines()
    hp = int(hp_line.split(":")[1])
    damage = int(damage_line.split(":")[1])
    boss = Player(hp, 0, 0, damage)
    game = GameState(player, boss)

    states = [game]
    heapq.heapify(states)

    while states:
        game = heapq.heappop(states)
        if game_over(game) and game.boss.hp == 0:
            break
        elif game_over(game):
            continue

        for move in available_moves(game):
            heapq.heappush(states, progress(game, move))

    return game.total_mana


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 22),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize("inp,result", [(aoc.get_input(2015, 22), 953)])
def test_solve(inp, result):
    assert result == solve(inp)
