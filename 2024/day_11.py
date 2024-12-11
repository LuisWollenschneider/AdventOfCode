from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 11,
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
    inp = [int(e) for e in inp_content.split()]

    return inp


@functools.lru_cache(maxsize=2**16)
def stone_production(n, remaining_blinks):
    if remaining_blinks == 0:
        return 1

    if n == 0:
        return stone_production(1, remaining_blinks - 1)
    elif (n_len := len(str_n := str(n))) % 2 == 0:
        return (stone_production(int(str_n[:n_len // 2]), remaining_blinks - 1) +
                stone_production(int(str_n[n_len // 2:]), remaining_blinks - 1))
    else:
        return stone_production(n * 2024, remaining_blinks - 1)


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return sum(map(lambda x: stone_production(x, 25), parse_input(input_str)))


@aoc_comm(settings, level=2, test_case=False)
def solve_l2(input_str) -> Optional[int]:
    return sum(map(lambda x: stone_production(x, 75), parse_input(input_str)))


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
