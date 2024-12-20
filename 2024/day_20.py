from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 20,
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
    start = None
    end = None
    walls = set()
    size_x = inp_content.find("\n")
    size_y = inp_content.count("\n") + 1
    for y, line in enumerate(inp_content.split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
            elif c == "#":
                walls.add((x, y))

    return start, end, walls, (size_x, size_y)


def bfs(start: list[tuple], end, size: tuple, walls):
    visited = defaultdict(int)

    queue = PriorityQueue()
    for s in start:
        queue.put(s)

    while not queue.empty():
        d, pos = queue.get()

        if pos[0] < 0 or pos[0] >= size[0] or pos[1] < 0 or pos[1] > size[1]:
            continue
        if pos in walls:
            continue
        if pos in visited:
            continue
        visited[pos] = d

        if pos == end:
            return visited, d

        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + i, pos[1] + j)
            queue.put((d + 1, new_pos))

    return visited, None


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step(pos):
    return {(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)}


def solve(input_str, cheat_duration, threshold: tuple):
    start, end, walls, size = parse_input(input_str)

    test_input = size == (15, 15)

    visited, d = bfs([(0, start)], end, size, walls)

    max_distance = d - threshold[test_input]

    rem_path, _ = bfs([(0, end)], (-1, -1), size, walls)

    faster_routes = 0
    for p, pd in visited.items():
        if distance(p, end) + pd > d:
            continue
        s = {p}
        prev = s
        for i in range(cheat_duration):
            new_s = set(itertools.chain(*map(step, prev)))
            for ns in new_s.difference(s):
                if ns not in rem_path:
                    continue
                if rem_path[ns] + pd + i + 1 <= max_distance:
                    faster_routes += 1
            s |= new_s
            prev = new_s

    return faster_routes


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return solve(input_str, 2, (100, 1))


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    return solve(input_str, 20, (100, 50))


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
