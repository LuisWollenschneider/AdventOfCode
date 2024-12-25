from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 25,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import log10
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    patterns = inp_content.split("\n\n")
    locks = []
    keys = []
    lock_height = patterns[0].count("\n") - 1
    for pattern in patterns:
        rows = pattern.split("\n")
        heights = []
        for x in range(len(rows[0])):
            heights.append(sum(1 for y in range(len(rows)) if rows[y][x] == "#") - 1)
        if set(rows[0]) == {'#'}:
            locks.append(heights)
        if set(rows[-1]) == {'#'}:
            keys.append(heights)

    return locks, keys, lock_height


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    locks, keys, lock_height = parse_input(input_str)

    fit = 0
    for key in keys:
        for lock in locks:
            if any(k + l > lock_height for k, l in zip(key, lock)):
                continue
            fit += 1
    return fit


@aoc_comm(settings, level=2, test_case=False)
def solve_l2(input_str) -> Optional[int]:
    return 0


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
