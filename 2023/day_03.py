from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 3,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def is_next_to_part(x, y, inp):
    for i in range(-1, 2):
        if x+i < 0 or x+i >= len(inp):
            continue
        for j in range(-1, 2):
            if y+j < 0 or y+j >= len(inp[0]):
                continue
            if i == j == 0:
                continue
            if inp[x+i][y+j].isdigit():
                continue
            if inp[x+i][y+j] == ".":
                continue
            return True
    return False


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = input_str.split('\n')

    s = 0

    for i, line in enumerate(inp):
        for j in range(len(line)):
            char = line[j]
            if not char.isdigit():
                continue
            if not is_next_to_part(i, j, inp):
                continue
            start, end = j, j
            while start > 0 and line[start - 1].isdigit():
                start -= 1
            while end < len(line) - 1 and line[end + 1].isdigit():
                end += 1
            s += int(line[start:end+1])
            line = line[:start] + ("." * (end - start + 1)) + line[end+1:]

    return s # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def get_adjacent(inp, x, y):
    res = []
    for i in range(-1, 2):
        res.append([])
        if x+i < 0 or x+i >= len(inp):
            res[-1] = "." * 3
            continue
        for j in range(-1, 2):
            if y+j < 0 or y+j >= len(inp[0]):
                res[-1].append(".")
                continue
            if i == j == 0:
                res[-1].append(".")
                continue
            res[-1].append(inp[x+i][y+j])
    return res


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = input_str.split('\n')

    s = 0
    for i, line in enumerate(inp):
        for j, char in enumerate(line):
            if char != "*":
                continue
            adj = get_adjacent(inp, i, j)
            numbers = 0
            coords = []
            for l, row in enumerate(adj):
                for k in range(len(row)):
                    if row[k].isdigit():
                        numbers += 1
                        coords.append((i + l - 1, j + k - 1))
                    while k < len(row) and row[k].isdigit():
                        row[k] = "."
                        k += 1
            if numbers != 2:
                continue
            m = 1
            for coord_x, coords_y in coords:
                start, end = coords_y, coords_y
                while start > 0 and inp[coord_x][start - 1].isdigit():
                    start -= 1
                while end < len(inp[coord_x]) - 1 and inp[coord_x][end + 1].isdigit():
                    end += 1
                m *= int(inp[coord_x][start:end + 1])
            s += m
    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
