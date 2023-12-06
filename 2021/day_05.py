from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 5,
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
    inp_content = [e.split(" -> ") for e in inp_content.split("\n")]
    return inp_content

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = [0] * 1_000_000
    for p1, p2 in inp:
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        if x1 == x2 or y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    ans[x * 1000 + y] += 1

    return len([el for el in ans if el > 1])  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = [0] * 1_000_000
    for p1, p2 in inp:
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        if x1 == x2 or y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    ans[x * 1000 + y] += 1
        if max(x1, x2) - min(x1, x2) == max(y1, y2) - min(y1, y2):
            for i in range(max(x1, x2) - min(x1, x2) + 1):
                if x1 > x2:
                    x = max(x1, x2) - i
                else:
                    x = min(x1, x2) + i
                if y1 > y2:
                    y = max(y1, y2) - i
                else:
                    y = min(y1, y2) + i
                ans[x * 1000 + y] += 1

    return len([el for el in ans if el > 1])


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
