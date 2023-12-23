from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 23,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


class Node:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.children = []
        self.dist = 0


def parse_input(inp_content, slippery=True):
    inp_content = inp_content.strip()
    # add further input processing here...
    nodes = {}

    height = len(inp_content.split("\n"))
    width = len(inp_content.split("\n")[0])

    for y, line in enumerate(inp_content.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                continue
            nodes[(x, y)] = Node(x, y, c)

    for n in nodes.values():
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (n.x + dx, n.y + dy) not in nodes:
                continue
            node = nodes[(n.x + dx, n.y + dy)]

            if slippery:
                if node.c == "<" and dx == 1:
                    continue
                if node.c == ">" and dx == -1:
                    continue
                if node.c == "^" and dy == 1:
                    continue
                if node.c == "v" and dy == -1:
                    continue

            n.children.append(node)

    furthest = {}
    for n in nodes.values():
        furthest[n] = furthest_node(n)

    reachable = {nodes[(1, 0)]}

    while True:
        new_reachable = set()
        for r in reachable:
            new_reachable.add(r)
            for n, d in furthest[r]:
                new_reachable.add(n)
        if new_reachable == reachable:
            break
        reachable = new_reachable

    knots = {r: furthest[r] for r in reachable}

    return knots, nodes[(1, 0)], nodes[(width - 2, height - 1)]


def furthest_node(start):
    res = []

    queue = []
    for c in start.children:
        queue.append((c, 1, {start}))

    while queue:
        node, dist, visited = queue.pop(0)

        if node in visited:
            continue
        visited = visited.copy()
        visited.add(node)

        children = list(filter(lambda n: n not in visited, node.children))
        if len(children) == 1:
            queue.append((children[0], dist + 1, visited))
        else:
            res.append((node, dist))

    return res


def longest_path(knots, start):
    queue = []
    for c, d in knots[start]:
        queue.append((c, d, {start}))

    while queue:
        node, dist, visited = queue.pop()

        if node in visited:
            continue

        visited = visited.copy()
        visited.add(node)

        node.dist = max(node.dist, dist)

        for rn, d in knots[node]:
            if rn in visited:
                continue
            queue.append((rn, dist + d, visited))


@aoc_comm(settings, level=1, debug=True)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    knots, start, end = parse_input(input_str, True)

    longest_path(knots, start)

    return end.dist  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2, debug=True)
def solve_l2(input_str) -> Optional[int]:
    knots, start, end = parse_input(input_str, False)

    longest_path(knots, start)

    return end.dist


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
