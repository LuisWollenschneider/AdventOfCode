from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 12,
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

    grid = {(x, y): c for y, row in enumerate(inp_content.split('\n')) for x, c in enumerate(row)}

    seen = set()

    def flood(x_, y_, c_):
        if (x_, y_) in seen:
            return set()
        if grid.get((x_, y_), None) != c_:
            return set()

        seen.add((x_, y_))
        area = {(x_, y_)}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            area |= flood(x_ + dx, y_ + dy, c_)

        return area

    plots = []
    for (x, y), c in grid.items():
        plot = flood(x, y, c)
        if plot:
            plots.append(plot)

    return plots


def edges(x, y, plot):
    return [(x + dx, y + dy, dx, dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)) if (x + dx, y + dy) not in plot]


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    plots = parse_input(input_str)

    s = 0
    for p in plots:
        perimeter = 0
        for x, y in p:
            perimeter += len(edges(x, y, p))
        s += perimeter * len(p)

    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    plots = parse_input(input_str)

    s = 0
    for p in plots:
        sides = 0
        es = []
        for x, y in p:
            es += edges(x, y, p)

        while es:
            x, y, dx, dy = es[0]

            def propagate(x_, y_):
                if (x_, y_, dx, dy) not in es:
                    return

                es.remove((x_, y_, dx, dy))

                if dx == 0:
                    propagate(x_ + 1, y_)
                    propagate(x_ - 1, y_)
                else:
                    propagate(x_, y_ + 1)
                    propagate(x_, y_ - 1)

            propagate(x, y)
            sides += 1

        s += sides * len(p)

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
