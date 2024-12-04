from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 2,
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
    inp_content = [list(map(int, e.split())) for e in inp_content.split("\n")]

    return inp_content


def all_increasing(lst):
    return all(lst[i] < lst[i + 1] for i in range(len(lst) - 1))


def all_decreasing(lst):
    return all(lst[i] > lst[i + 1] for i in range(len(lst) - 1))


def valid_distance(lst):
    return all(abs(lst[i] - lst[i + 1]) <= 3 for i in range(len(lst) - 1))


def is_safe(lst):
    return (all_increasing(lst) or all_decreasing(lst)) and valid_distance(lst)


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    levels = parse_input(input_str)

    return len(list(filter(lambda x: is_safe(x), levels)))


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    levels = parse_input(input_str)

    s = 0
    for level in levels:
        if is_safe(level):
            s += 1
            continue
        l = level.copy()
        for i in range(len(level)):
            if is_safe(l[:i] + l[i + 1:]):
                s += 1
                break

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
