from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 14,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..

    robots = []
    for l in inp_content.split("\n"):
        x, y, vx, vy = map(int, re.findall(r'-?\d+', l))
        robots.append(Robot(x, y, vx, vy))

    return robots


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    robots = parse_input(input_str)
    size_x, size_y = (101, 103) if len(robots) != 12 else (11, 7)

    end_positions = []
    for r in robots:
        x = (r.x + r.vx * 100) % size_x
        y = (r.y + r.vy * 100) % size_y
        end_positions.append((x, y))

    s = 1
    for x_r1, x_r2 in [(0, size_x // 2 - 1), (size_x // 2 + 1, size_x)]:
        for y_r1, y_r2 in [(0, size_y // 2 - 1), (size_y // 2 + 1, size_y)]:
            print(x_r1, x_r2, y_r1, y_r2, sum((x_r1 <= x <= x_r2 and y_r1 <= y <= y_r2) for x, y in end_positions))
            s *= sum((x_r1 <= x <= x_r2 and y_r1 <= y <= y_r2) for x, y in end_positions)

    return s


@aoc_comm(settings, level=2, test_case=False)
def solve_l2(input_str) -> Optional[int]:
    robots = parse_input(input_str)
    size_x, size_y = (101, 103) if len(robots) != 12 else (11, 7)

    s = 0
    while True:
        positions = set()
        for r in robots:
            x = (r.x + r.vx * s) % size_x
            y = (r.y + r.vy * s) % size_y
            positions.add((x, y))

        if len(positions) != len(robots):
            s += 1
            continue

        for y in range(size_y):
            for x in range(size_x):
                print(" " if (x, y) not in positions else "#", end="")
            print()

        break

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
