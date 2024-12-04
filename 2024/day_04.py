from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 4,
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


def search(x, y, dir_x, dir_y, grid, rest):
    if not rest:
        return True
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return False
    if grid[y][x] != rest[0]:
        return False
    return search(x + dir_x, y + dir_y, dir_x, dir_y, grid, rest[1:])


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    grid = parse_input(input_str)

    s = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            for dir_x in [-1, 0, 1]:
                for dir_y in [-1, 0, 1]:
                    if dir_x == 0 and dir_y == 0:
                        continue
                    if search(x, y, dir_x, dir_y, grid, "XMAS"):
                        s += 1

    return s


def get_cell(grid, x, y):
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return None
    return grid[y][x]


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    grid = parse_input(input_str)

    s = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "A":
                continue

            diag_1 = {get_cell(grid, x - 1, y - 1), get_cell(grid, x + 1, y + 1)}
            diag_2 = {get_cell(grid, x + 1, y - 1), get_cell(grid, x - 1, y + 1)}

            if diag_1 == {"M", "S"} and diag_2 == {"M", "S"}:
                s += 1

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
