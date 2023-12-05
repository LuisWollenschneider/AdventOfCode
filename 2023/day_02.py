from dataclasses import dataclass

from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 2,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


@dataclass
class Selection:
    red: int
    green: int
    blue: int

@dataclass
class Game:
    id: int
    selections: list[Selection]


def parse_input(input_str):
    games = []
    for line in input_str.split('\n'):
        game_id, selections = line.split(":")
        game_id = int(game_id.split(" ")[1])
        selections = selections.split(";")

        game = Game(game_id, [])

        for selection in selections:
            red, green, blue = 0, 0, 0
            for color in selection.split(","):
                if "red" in color:
                    red = int(color.strip().split(" ")[0])
                elif "green" in color:
                    green = int(color.strip().split(" ")[0])
                elif "blue" in color:
                    blue = int(color.strip().split(" ")[0])
            game.selections.append(Selection(red, green, blue))

        games.append(game)
    return games


def game_possible(game, red, green, blue):
    for selection in game.selections:
        if selection.red > red or selection.green > green or selection.blue > blue:
            return 0
    return game.id


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    games = parse_input(input_str)

    return sum(map(lambda g: game_possible(g, 12, 13, 14), games)) # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def minimal_cube_power(game):
    red, green, blue = 0, 0, 0
    for selection in game.selections:
        red = max(red, selection.red)
        green = max(green, selection.green)
        blue = max(blue, selection.blue)
    return red * green * blue


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    games = parse_input(input_str)

    return sum(map(minimal_cube_power, games))


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
