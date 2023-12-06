from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 15,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
import numpy as np

grid: np.array = np.array([])
solved_grid: np.array = np.array([])
grid_size = 100
solved_size = 100


def parse_input(inp_content, factor=1):
    global grid, solved_grid, grid_size, solved_size
    inp_content = inp_content.strip()
    # add further input processing here..
    grid = []
    for e in inp_content.split("\n"):
        grid.append([])
        for l in e:
            grid[-1].append(int(l))
    grid_size = len(grid)
    grid = np.array(grid)
    solved_grid = []
    for x in range(grid_size * factor):
        solved_grid.append([])
        for y in range(grid_size * factor):
            solved_grid[x].append(-1)
    solved_size = len(solved_grid)
    solved_grid = np.array(solved_grid)
    return None


def in_bounds(x, y):
    return 0 <= x < solved_size and 0 <= y < solved_size


def get_calculated_risk(x, y) -> Optional[int]:
    if solved_grid[x, y] != -1:
        return solved_grid[x, y]
    return None


def adjusted_min_risk(x, y) -> Optional[int]:
    if x == 0 and y == 0:
        return 0
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    risks = []
    for x_, y_ in neighbors:
        if in_bounds(x + x_, y + y_):
            r = get_calculated_risk(x + x_, y + y_)
            if r is not None:
                risks.append(r)
    if not risks:
        return None
    return min(risks)


def get_value(x, y):
    rep = x // grid_size + y // grid_size
    x = x % grid_size
    y = y % grid_size
    ret = grid[x, y] + rep
    if ret >= 10:
        ret -= 9
    return ret


def solve_grid():
    changes = 1
    while changes != 0:
        changes = 0
        for x in range(solved_size):
            for y in range(solved_size):
                r_min = solved_grid[x, y]
                ad_min = adjusted_min_risk(x, y)
                r = get_value(x, y) + ad_min
                if r < r_min or r_min == -1:
                    # print(f"({x}, {y}) {solved_grid[x][y]} -> {r}")
                    solved_grid[x][y] = r
                    changes += 1
        print(f"{changes} changes performed!")


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    parse_input(input_str)
    solved_grid[0, 0] = 0
    solve_grid()
    return solved_grid[-1, -1]


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    parse_input(input_str, 5)
    solved_grid[0, 0] = 0
    solve_grid()
    return solved_grid[-1, -1]


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
