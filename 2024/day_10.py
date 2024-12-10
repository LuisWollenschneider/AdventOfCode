from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 10,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
from queue import PriorityQueue


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp = [list(map(int, e)) for e in inp_content.split("\n")]

    return inp


def walk(grid, x, y, unique=False):
    queue = PriorityQueue()
    queue.put((-1, x, y))
    end_points = []
    while not queue.empty():
        h, x, y = queue.get()
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            continue
        height = grid[y][x]
        if h + 1 != height:
            continue
        if height == 9:
            end_points.append((x, y))
            continue

        queue.put((height, x + 1, y))
        queue.put((height, x - 1, y))
        queue.put((height, x, y + 1))
        queue.put((height, x, y - 1))

    return len(end_points if unique else set(end_points))


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    s = 0
    for y, row in enumerate(inp):
        for x, height in enumerate(row):
            if height == 0:
                s += walk(inp, x, y)

    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    s = 0
    for y, row in enumerate(inp):
        for x, height in enumerate(row):
            if height == 0:
                s += walk(inp, x, y, True)

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
