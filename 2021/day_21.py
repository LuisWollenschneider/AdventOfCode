from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 21,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [int(e[-1]) for e in inp_content.split("\n")]
    return inp_content


class Die:
    def __init__(self):
        self.c = 1
        self.rolled = 0

    def roll(self) -> int:
        self.rolled += 1
        c = self.c
        self.c += 1
        if self.c > 100:
            self.c = 1
        return c

    def roll_n(self, n=3):
        return sum([self.roll() for _ in range(n)])


class DiracDice(Die):
    def roll_n(self, n=3) -> int:
        return n


class Player:
    def __init__(self, position: int, score=0):
        self.position: int = position
        self.score = score

    def turn(self, die: Die, n=3):
        self.position += die.roll_n(n)
        self.position %= 10
        if self.position == 0:
            self.position = 10
        self.score += self.position

    def won(self, n=1_000):
        return self.score >= n

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    players: list[Player] = []
    for ee in inp:
        players.append(Player(ee))

    die = Die()
    c = 0
    while not any([p.won() for p in players]):
        players[c].turn(die)
        c = (c + 1) % 2
    loser = None
    for p in players:
        if not p.won():
            loser = p
            break

    return die.rolled * loser.score  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)
    d = {(inp[0], inp[1], 0, 0): 1}
    final = defaultdict(int)
    die = DiracDice()
    c = 0
    while True:
        d_ = defaultdict(int)
        for k, v in d.items():
            for res, x in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
                p = Player(k[c], k[c+2])
                p.turn(die, res)
                if p.won(21):
                    final[c] += v * x
                else:
                    if c == 0:
                        d_[(p.position, k[1], p.score, k[3])] += v * x
                    else:
                        d_[(k[0], p.position, k[2], p.score)] += v * x
        d = d_.copy()
        if not d:
            break
        c = (c + 1) % 2

    return max(final.values())


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
