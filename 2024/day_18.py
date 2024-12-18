from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 18,
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

    return [tuple(map(int, e.split(","))) for e in inp_content.split("\n")]


def bfs(start, end, size, obstacles):
    visited = defaultdict(int)
    queue = PriorityQueue()
    queue.put((0, (start, [])))

    while not queue.empty():
        d, (pos, path) = queue.get()

        if pos[0] < 0 or pos[0] > size or pos[1] < 0 or pos[1] > size:
            continue

        if visited.get(pos, float("inf")) <= d:
            continue

        if pos in obstacles:
            continue

        visited[pos] = d
        new_path = path.copy() + [pos]

        if pos == end:
            return d

        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + i, pos[1] + j)
            queue.put((d + 1, (new_pos, new_path)))

    return None


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[str]:  # input data will be passed to this as string
    coords = parse_input(input_str)

    if len(coords) == 25:
        size = 6
        first_n = 12
    else:
        size = 70
        first_n = 1024

    return bfs((0, 0), (size, size), size, coords[:first_n])


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[str]:
    coords = parse_input(input_str)

    if len(coords) == 25:
        size = 6
    else:
        size = 70

    first_n = 0
    while True:
        if bfs((0, 0), (size, size), size, coords[:first_n]) is None:
            return ','.join(map(str, coords[first_n - 1]))
        first_n += 1


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
