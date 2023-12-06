from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 3,
    'year': 2018,
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
    inp_content = [e for e in inp_content.split("\n")]
    return inp_content

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    A = set()
    D = set()
    for ee in inp:
        _, _, c, r = ee.split(" ")
        cx, cy = map(int, c[:-1].split(","))
        rx, ry = map(int, r.split("x"))
        for x in range(cx, cx+rx):
            for y in range(cy, cy+ry):
                if (x, y) in A:
                    D.add((x, y))
                A.add((x,y))

    return len(D)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    A = defaultdict(set)
    for ee in inp:
        id_, _, c, r = ee.split(" ")
        cx, cy = map(int, c[:-1].split(","))
        rx, ry = map(int, r.split("x"))
        for x in range(cx, cx+rx):
            for y in range(cy, cy+ry):
                A[(x, y)].add(id_)
    for ee in inp:
        id_, _, c, r = ee.split(" ")
        cx, cy = map(int, c[:-1].split(","))
        rx, ry = map(int, r.split("x"))
        ok = True
        for x in range(cx, cx+rx):
            for y in range(cy, cy+ry):
                if len(A[(x, y)]) > 1:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return int(id_[1:])
    return None


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
