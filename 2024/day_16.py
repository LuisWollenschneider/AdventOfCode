from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 16,
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
    start = (0, 0)
    end = (0, 0)
    path = set()

    for y, row in enumerate(inp_content.split("\n")):
        for x, cell in enumerate(row):
            if cell == "#":
                continue
            path.add((x, y))
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)

    return start, end, path


def bfs(start, end, path):
    queue = [(start, (1, 0), 0, set())]
    visited = defaultdict(int)

    end_steps = float("inf")
    end_path = set()

    while queue:
        pos, d, steps, p = queue.pop(0)
        if pos not in path:
            continue

        if visited[pos] and visited[pos] < steps - 1001:  # Hacky shit because the turns mess up the step count at intersections...
            continue
        visited[pos] = steps

        p = p.copy() | {pos}
        if pos == end:
            if steps == end_steps:
                end_path |= p
            elif steps < end_steps:
                end_steps = steps
                end_path = p
            continue

        queue.append(((pos[0] + d[0], pos[1] + d[1]), d, steps + 1, p))
        if d[0] == 0:
            queue.append(((pos[0] + 1, pos[1]), (1, 0), steps + 1001, p))
            queue.append(((pos[0] - 1, pos[1]), (-1, 0), steps + 1001, p))
        else:
            queue.append(((pos[0], pos[1] + 1), (0, 1), steps + 1001, p))
            queue.append(((pos[0], pos[1] - 1), (0, -1), steps + 1001, p))

    return end_steps, end_path


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return bfs(*parse_input(input_str))[0]


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    return len(bfs(*parse_input(input_str))[1])


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
