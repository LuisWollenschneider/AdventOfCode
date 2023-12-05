from utils import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 7,
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
    inp_content = [int(e) for e in inp_content.split(",")]
    return inp_content


def align(crabs, position):
    return sum([abs(position - c) for c in crabs])


def align2(crabs, position):
    return sum([(abs(position - c) * (abs(position - c) + 1)) // 2 for c in crabs])


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    return min([align(inp, h) for h in range(min(inp), max(inp) + 1)])  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)
    return min([align2(inp, h) for h in range(min(inp), max(inp) + 1)])


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
