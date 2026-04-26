from __future__ import annotations

import re
from collections.abc import Iterator
from functools import reduce
from operator import mul
from typing import NamedTuple

import aoc

RE_INGREDIENT = re.compile(
    r"(?P<name>\w+): "
    r"capacity (?P<capacity>-?\d+), "
    r"durability (?P<durability>-?\d+), "
    r"flavor (?P<flavor>-?\d+), "
    r"texture (?P<texture>-?\d+), "
    r"calories (?P<calories>-?\d+)"
)


class Ingredient(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_txt(cls, line: str) -> Ingredient:
        m = RE_INGREDIENT.fullmatch(line)
        assert m is not None
        return Ingredient(
            int(m.group("capacity")),
            int(m.group("durability")),
            int(m.group("flavor")),
            int(m.group("texture")),
            int(m.group("calories")),
        )


Teaspoons = int
Recipe = set[tuple[Ingredient, Teaspoons]]


def all_recipes(
    ingredients: tuple[Ingredient, ...], total: Teaspoons = 100
) -> Iterator[Recipe]:
    if len(ingredients) == 1 and total > 0:
        yield {(ingredients[0], total)}
    elif total > 0 and ingredients:
        yield from all_recipes(ingredients[1:], total)
        yield {(ingredients[0], total)}
        for teaspoons in range(1, total + 1):
            for subrecipe in all_recipes(ingredients[1:], total - teaspoons):
                yield {(ingredients[0], teaspoons), *subrecipe}


def rate_recipe(recipe: Recipe) -> int:
    return reduce(
        mul,
        map(
            lambda x: max(x, 0),
            (
                sum(
                    ingredient[category] * teaspoons for ingredient, teaspoons in recipe
                )
                for category in range(0, 4)
            ),
        ),
    )


def recipe_calories(recipe: Recipe):
    return sum(ingredient.calories * teaspoons for ingredient, teaspoons in recipe)


def solve(inp: str) -> int:
    ingredients = tuple(Ingredient.from_txt(line) for line in inp.strip().splitlines())
    recipes_500_cal = filter(
        lambda recipe: recipe_calories(recipe) == 500, all_recipes(ingredients)
    )
    return max(map(rate_recipe, recipes_500_cal))


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(solve, 2015, 15),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "line,ingredient",
    [
        (
            "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
            Ingredient(-1, -2, 6, 3, 8),
        ),
        (
            "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3",
            Ingredient(2, 3, -2, -1, 3),
        ),
        (
            "Tofu: capacity 0, durability 0, flavor 0, texture 0, calories 0",
            Ingredient(0, 0, 0, 0, 0),
        ),
    ],
)
def test_ingredient_parse(line, ingredient):
    assert ingredient == Ingredient.from_txt(line)


@pytest.mark.parametrize(
    "recipe,score",
    [
        (
            {
                (Ingredient(-1, -2, 6, 3, 8), 44),
                (Ingredient(2, 3, -2, -1, 3), 56),
            },
            62842880,
        ),
        (
            {
                (Ingredient(-1, -1, -1, -1, -1), 44),
                (Ingredient(-1, -1, -1, -1, -1), 56),
            },
            0,
        ),
    ],
)
def test_recipe_score(recipe, score):
    assert score == rate_recipe(recipe)


@pytest.mark.parametrize(
    "ingredients, num_recipes",
    [
        ((), 0),
        ((Ingredient(0, 0, 0, 0, 0),), 1),
        ((Ingredient(0, 0, 0, 0, 0), Ingredient(0, 0, 0, 0, 0)), 101),
    ],
)
def test_all_recipes(ingredients, num_recipes):
    assert num_recipes == len(list(all_recipes(ingredients)))


@pytest.mark.parametrize(
    "inp,result",
    [
        (
            "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8\n"  # noqa: E501
            "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3\n",
            57600000,
        ),
        (aoc.get_input(2015, 15), 11171160),
    ],
)
def test_solve(inp, result):
    assert result == solve(inp)
