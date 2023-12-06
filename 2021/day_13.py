from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 13,
    'year': 2021,
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
    inp_content = [e for e in inp_content.split("\n\n")]
    inp_content[0] = [tuple(map(int, l.split(","))) for l in inp_content[0].split("\n")]
    inp_content[1] = inp_content[1].split("\n")
    return inp_content


def fold(sheet: list[tuple[int, int]], x=-1, y=-1) -> list[tuple[int, int]]:
    res = set()
    if x != -1:
        for i, d in enumerate(sheet):
            if d[0] > x:
                res.add((x - (d[0] % x if d[0] % x != 0 else x), d[1]))
            elif d[0] < x:
                res.add(d)
    elif y != -1:
        for i, d in enumerate(sheet):
            if d[1] > y:
                res.add((d[0], y - (d[1] % y if d[1] % y != 0 else y)))
            elif d[1] < y:
                res.add(d)
    return list(res)

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    # execute only step 1
    d = {"x": -1, "y": -1}
    d[inp[1][0][11]] = int(inp[1][0][13:])
    return len(fold(inp[0], d["x"], d["y"]))


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    for l in inp[1]:
        d = {"x": -1, "y": -1}
        d[l[11]] = int(l[13:])
        inp[0] = fold(inp[0], d["x"], d["y"])
    # compute max values x and y
    x_, y_ = 0, 0
    for d in inp[0]:
        if d[0] > x_:
            x_ = d[0]
        if d[1] > y_:
            y_ = d[1]
    # print result
    for j in range(y_ + 1):
        for i in range(x_ + 1):
            print("." if (i, j) not in inp[0] else "#", end="")
        print("")
    return None


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
