from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 2,
    'year': 2018,
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
    inp = parse_input(input_str)

    twice = 0
    thrice = 0
    for ee in inp:
        c = Counter(ee)
        if 2 in c.values():
            twice += 1
        if 3 in c.values():
            thrice += 1

    return twice * thrice  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    SEEN = set()
    for ee in inp:
        prev = None
        for i in range(len(ee)):
            seen = ee[:i] + ee[i+1:]
            if seen == prev:
                continue
            if seen in SEEN:
                return seen
            SEEN.add(seen)
            prev = seen

    return None


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
