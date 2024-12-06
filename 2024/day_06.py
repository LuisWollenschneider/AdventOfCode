from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 6,
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
    obstacles = {(x, y) for y, row in enumerate(inp_content.split("\n")) for x, cell in enumerate(row) if cell == "#"}
    starting_point = None
    dir_x, dir_y = 0, 0
    for y, row in enumerate(inp_content.split("\n")):
        for x, cell in enumerate(row):
            if cell != "." and cell != "#":
                starting_point = (x, y)
                if cell == "^":
                    dir_y = -1
                elif cell == "v":
                    dir_y = 1
                elif cell == "<":
                    dir_x = -1
                elif cell == ">":
                    dir_x = 1
                break

    return obstacles, (inp_content.index("\n"), len(inp_content.split("\n"))), starting_point, (dir_x, dir_y)


def turn(direction):
    if direction == (0, -1):
        return 1, 0
    if direction == (1, 0):
        return 0, 1
    if direction == (0, 1):
        return -1, 0
    if direction == (-1, 0):
        return 0, -1


def move(obstacles, from_point, direction):
    x, y = from_point
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if (new_x, new_y) in obstacles:
        return x, y
    return new_x, new_y


def print_map(obstacles, size_x, size_y, cur_pos, dir, visited):
    for y in range(size_y):
        for x in range(size_x):
            if (x, y) in obstacles:
                print("#", end="")
            elif (x, y) == cur_pos:
                if dir == (0, -1):
                    print("^", end="")
                elif dir == (1, 0):
                    print(">", end="")
                elif dir == (0, 1):
                    print("v", end="")
                elif dir == (-1, 0):
                    print("<", end="")
            elif (x, y) in visited:
                print("X", end="")
            else:
                print(".", end="")
        print()


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    obstacles, (size_x, size_y), starting_point, (dir_x, dir_y) = parse_input(input_str)

    visited = {starting_point}
    while True:
        new_point = move(obstacles, starting_point, (dir_x, dir_y))
        if new_point == starting_point:
            dir_x, dir_y = turn((dir_x, dir_y))
            continue
        if new_point[0] < 0 or new_point[0] >= size_x or new_point[1] < 0 or new_point[1] >= size_y:
            break
        visited.add(new_point)
        starting_point = new_point

    return len(visited)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    orig_obstacles, (size_x, size_y), orig_starting_point, orig_direction = parse_input(input_str)

    s = 0

    for y in range(size_y):
        for x in range(size_x):
            if (x, y) in orig_obstacles:
                continue
            if (x, y) == orig_starting_point:
                continue

            obstacles = orig_obstacles.copy()
            obstacles.add((x, y))
            starting_point = orig_starting_point
            direction = orig_direction
            visited = {(starting_point, direction)}
            while True:
                new_point = move(obstacles, starting_point, direction)
                if new_point == starting_point:
                    direction = turn(direction)
                    continue
                if new_point[0] < 0 or new_point[0] >= size_x or new_point[1] < 0 or new_point[1] >= size_y:
                    break
                if (new_point, direction) in visited:
                    s += 1
                    break
                visited.add((new_point, direction))
                starting_point = new_point

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
