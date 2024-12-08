from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 8,
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
    inp = defaultdict(list)
    for y, row in enumerate(inp_content.split("\n")):
        for x, antenna in enumerate(row):
            if antenna == ".":
                continue
            inp[antenna].append((x, y))

    return inp


def print_map(size_x, size_y, antennas, antinodes):
    for y in range(size_y):
        for x in range(size_x):
            if (x, y) in antinodes:
                print("#", end="")
            else:
                for a in antennas:
                    if (x, y) in antennas[a]:
                        print(a, end="")
                        break
                else:
                    print(".", end="")
        print()



@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    antennas = parse_input(input_str)
    size_x = input_str.find("\n")
    size_y = input_str.strip().count("\n") + 1
    antinodes = set()
    for antenna in antennas:
        for i, (x1, y1) in enumerate(antennas[antenna]):
            for x2, y2 in antennas[antenna][i+1:]:
                print(antenna, (x1, y1), (x2, y2))
                dx = x2 - x1
                dy = y2 - y1
                antinodes.add((x1 - dx, y1 - dy))
                antinodes.add((x2 + dx, y2 + dy))

    antinodes = set(filter(lambda x: 0 <= x[0] < size_x and 0 <= x[1] < size_y, antinodes))

    return len(antinodes)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    antennas = parse_input(input_str)
    size_x = input_str.find("\n")
    size_y = input_str.strip().count("\n") + 1
    antinodes = set()
    for antenna in antennas:
        for i, (x1, y1) in enumerate(antennas[antenna]):
            for x2, y2 in antennas[antenna][i + 1:]:
                dx = x2 - x1
                dy = y2 - y1
                c = 0
                while True:
                    x = x1 + dx * c
                    y = y1 + dy * c
                    if x < 0 or x >= size_x or y < 0 or y >= size_y:
                        break
                    antinodes.add((x, y))
                    c += 1
                c = 1
                while True:
                    x = x1 - dx * c
                    y = y1 - dy * c
                    if x < 0 or x >= size_x or y < 0 or y >= size_y:
                        break
                    antinodes.add((x, y))
                    c += 1

    return len(antinodes)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
