from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day': 1,
    'year': 2019,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [int(e) for e in inp_content.split("\n")]
    return inp_content


def fuel(n):
    return max(floor(n / 3) - 2, 0)

    
@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = 0
    for ee in inp:
        ans += fuel(ee)

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    ans = 0
    for ee in inp:
        f = fuel(ee)
        while f != 0:
            ans += f
            f = fuel(f)
    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
