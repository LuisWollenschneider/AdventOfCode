from copy import deepcopy

from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 25,
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
    inp_content = [list(e) for e in inp_content.split("\n")]
    return inp_content


def step(inp: list[list[str]]):
    l = len(inp[0])
    field = deepcopy(inp)
    moved = defaultdict(list)
    changed = False
    for i in range(len(inp)):
        for j, c in enumerate(field[i]):
            if j in moved[i]:
                continue
            if inp[i][j] == ">":
                if inp[i][(j + 1) % l] == ".":
                    field[i][j] = "."
                    field[i][(j + 1) % l] = ">"
                    changed = True
                    moved[i].append((j + 1) % l)
    l = len(inp)
    moved = defaultdict(list)
    field_ = deepcopy(field)
    for i in range(len(inp)):
        for j, c in enumerate(field[i]):
            if j in moved[i]:
                continue
            if c == "v":
                if field[(i + 1) % l][j] == ".":
                    field_[i][j] = "."
                    field_[(i + 1) % l][j] = "v"
                    changed = True
                    moved[(i + 1) % l].append(j)
    return field_, changed


@aoc_comm(settings, level=1)
def solve_l1(input_str): # -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    c = 0
    while True:
        inp, b = step(inp)
        c += 1
        if not b:
            break

    return c  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()


if __name__ == '__main__':
    main()
