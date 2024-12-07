from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 7,
    'year': 2024,
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
    inp = [[list(map(int, p.split())) for p in e.split(": ")] for e in inp_content.split("\n")]

    return inp


def validate(v, remaining, goal, operators):
    if len(remaining) == 0:
        return v == goal

    if v > goal:
        return False

    next_v = remaining[0]
    new_remaining = remaining[1:]
    for op in operators:
        if validate(op(v, next_v), new_remaining, goal, operators):
            return True

    return False


def solve(input_str, operators):
    inp = parse_input(input_str)
    s = 0
    for goal, nums in inp:
        if validate(nums[0], nums[1:], goal[0], operators):
            s += goal[0]

    return s


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    operators = [int.__add__, int.__mul__]
    return solve(input_str, operators)


def concat(x, y):
    return x * (10 ** (floor(log10(y)) + 1)) + y


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    operators = [int.__add__, int.__mul__, concat]
    return solve(input_str, operators)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
