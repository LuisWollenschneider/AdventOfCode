from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 3,
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

    return inp_content


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)", input_str)

    s = 0
    for m in matches:
        a, b = re.search(r"\d{1,3},\d{1,3}", m).group(0).split(",")
        s += int(a) * int(b)

    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    matches = re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", input_str)

    s = 0
    enabled = True
    for m in matches:
        if m == "do()":
            enabled = True
            continue
        if m == "don't()":
            enabled = False
            continue
        if not enabled:
            continue
        a, b = re.search(r"\d{1,3},\d{1,3}", m).group(0).split(",")
        s += int(a) * int(b)

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
