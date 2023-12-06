from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 12,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


caves = {}


def parse_input(inp_content):
    global caves
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [e.split("-") for e in inp_content.split("\n")]
    caves = defaultdict(set)
    for s, e in inp_content:
        caves[s].add(e)
        caves[e].add(s)
    return None


@functools.cache
def find_path(cave: str, path: tuple, count: int = 1) -> int:
    if cave == "end":
        return 1
    if cave.islower():
        if cave in path:
            if cave == "start":
                return 0
            if any([v >= count for v in Counter(path).values()]):
                return 0
        path = (*path, cave)
    return sum([find_path(c, path, count=count) for c in caves[cave]])


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    find_path.cache_clear()
    parse_input(input_str)
    # return find_path("start", defaultdict(int))  # if 'ans' is None answer won't be submitted, else it will submit after confirmation
    return find_path("start", tuple())  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    find_path.cache_clear()
    parse_input(input_str)
    # return find_path("start", defaultdict(int), count=2)
    return find_path("start", tuple(), count=2)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
