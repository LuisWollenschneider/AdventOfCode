from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 1,
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
    inp_content = [e for e in inp_content.split("\n")]

    left, right = [], []
    for e in inp_content:
        e1, e2 = e.split("   ")
        left.append(int(e1))
        right.append(int(e2))
    return left, right


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    left, right = parse_input(input_str)
    left = sorted(left)
    right = sorted(right)
    s = 0
    for e1, e2 in zip(left, right):
        s += abs(e1 - e2)
    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    left, right = parse_input(input_str)

    s = 0
    for e1 in left:
        s += right.count(e1) * e1

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
