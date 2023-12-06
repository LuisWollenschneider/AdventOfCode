from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 9,
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
    inp_content = [e for e in inp_content.split("\n")]
    return inp_content


def get_basin_indices(inp: list[str]) -> list[tuple[int, int]]:
    basins = []
    for i, ee in enumerate(inp):
        for j, e in enumerate(ee):
            low = True
            if i > 0:
                if e >= inp[i - 1][j]:
                    low = False
            if i < len(inp) - 1:
                if e >= inp[i + 1][j]:
                    low = False
            if j > 0:
                if e >= inp[i][j-1]:
                    low = False
            if j < len(ee) - 1:
                if e >= inp[i][j + 1]:
                    low = False
            if low:
                basins.append((i, j))
    return basins

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = 0
    for i, j in get_basin_indices(inp):
        ans += 1 + int(inp[i][j])

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def get_higher_points(inp: list[str], n: int, i: int, j: int, l: Optional[list[tuple[int, int]]]) -> list[tuple[int, int]]:
    if i < 0 or i >= len(inp[0]):
        return l
    if j < 0 or j >= len(inp):
        return l
    if (i, j) in l:
        return l
    n_ = int(inp[i][j])
    if 9 > n_ > n:
        l.append((i, j))
        l = get_higher_points(inp, n_, i + 1, j, l)
        l = get_higher_points(inp, n_, i - 1, j, l)
        l = get_higher_points(inp, n_, i, j + 1, l)
        l = get_higher_points(inp, n_, i, j - 1, l)
    return l


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    basins = []
    for i, j in get_basin_indices(inp):
        basins.append(len(get_higher_points(inp, -1, i, j, [])))
    ans = 1
    for x in sorted(basins)[-3:]:
        ans *= x
    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
