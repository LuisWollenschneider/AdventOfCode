from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 19,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
from queue import PriorityQueue


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..

    towels, patterns = inp_content.split("\n\n")

    towels = towels.split(", ")
    patterns = patterns.split("\n")

    return towels, patterns


def constructable(towels: list[str], remaining_pattern: str):
    if not remaining_pattern:
        return True

    for t in towels:
        if remaining_pattern.startswith(t):
            if constructable(towels, remaining_pattern.removeprefix(t)):
                return True
    return False


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    towels, patterns = parse_input(input_str)

    return sum(constructable(towels, p) for p in patterns)


@functools.lru_cache(None)
def ways_to_construct(towels: tuple[str], remaining_pattern: str):
    if not remaining_pattern:
        return 1

    s = 0
    for t in towels:
        if remaining_pattern.startswith(t):
            s += ways_to_construct(towels, remaining_pattern.removeprefix(t))
    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    towels, patterns = parse_input(input_str)

    towels = tuple(towels)

    return sum(ways_to_construct(towels, p) for p in patterns)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
