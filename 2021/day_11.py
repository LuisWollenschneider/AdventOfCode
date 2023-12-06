from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 11,
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
    res = []
    for e in inp_content.split("\n"):
        res.append([])
        for o in e:
            res[-1].append(int(o))
    return res


def blink(i: int, j: int, grid: list[list[int]]) -> list[list[int]]:
    if not 0 <= i < len(grid):
        return grid
    if not 0 <= j < len(grid[0]):
        return grid
    grid[i][j] += 1
    if grid[i][j] != 10:
        return grid
    for i_ in [-1, 0, 1]:
        for j_ in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            grid = blink(i + i_, j + j_, grid)
    return grid


def step(grid: list[list[int]]) -> tuple[int, list[list[int]]]:
    blinks = 0
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            grid = blink(row, column, grid)
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] >= 10:
                blinks += 1
                grid[row][column] = 0
    return blinks, grid


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = 0
    for _ in range(100):
        b, inp = step(inp)
        ans += b

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = 0
    while sum([sum(row) for row in inp]) != 0:
        _, inp = step(inp)
        ans += 1

    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
