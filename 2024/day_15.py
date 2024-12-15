from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 15,
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
    robot = (0, 0)
    walls = set()
    boxes = set()

    grid, movements = inp_content.split("\n\n")

    for y, row in enumerate(grid.split("\n")):
        for x, cell in enumerate(row):
            if cell == "#":
                walls.add((x, y))
            elif cell == "@":
                robot = (x, y)
            elif cell == "O":
                boxes.add((x, y))

    movements = movements.strip().replace("\n", "")

    return robot, walls, boxes, movements


def direction(m):
    if m == "^":
        return 0, -1
    elif m == "v":
        return 0, 1
    elif m == "<":
        return -1, 0
    elif m == ">":
        return 1, 0


def move(pos, boxes, walls, d) -> bool:
    if pos in walls:
        return False
    if pos in boxes:
        new_pos = (pos[0] + d[0], pos[1] + d[1])
        if not move(new_pos, boxes, walls, d):
            return False
        boxes.remove(pos)
        boxes.add(new_pos)
    return True


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    robot, walls, boxes, movements = parse_input(input_str)

    for m in movements:
        d = direction(m)
        boxes.add(robot)
        if move(robot, boxes, walls, d):
            robot = (robot[0] + d[0], robot[1] + d[1])
            boxes.remove(robot)
        else:
            boxes.remove(robot)

    return sum(x + 100 * y for x, y in boxes)


def move_wide(pos, boxes, walls, d) -> bool:
    affected_boxes = set()
    to_check: list = [(pos[0] + d[0], pos[1] + d[1])]
    if d[0] != 1:
        to_check.append((pos[0] + d[0] - 1, pos[1] + d[1]))

    while to_check:
        p = to_check.pop()
        if p in walls:
            return False
        if p in boxes:
            affected_boxes.add(p)
            if d[0]:
                to_check.append((p[0] + d[0] * 2, p[1]))
            if d[1]:
                to_check.append((p[0], p[1] + d[1]))
                to_check.append((p[0] - 1, p[1] + d[1]))
                to_check.append((p[0] + 1, p[1] + d[1]))

    for b in affected_boxes:
        boxes.remove(b)
    for b in affected_boxes:
        boxes.add((b[0] + d[0], b[1] + d[1]))

    return True


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    robot, walls, boxes, movements = parse_input(input_str)
    walls = {(x * 2, y) for x, y in walls}
    boxes = {(x * 2, y) for x, y in boxes}
    robot = (robot[0] * 2, robot[1])

    for m in movements:
        d = direction(m)
        if move_wide(robot, boxes, walls, d):
            robot = (robot[0] + d[0], robot[1] + d[1])

    return sum(x + 100 * y for x, y in boxes)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
