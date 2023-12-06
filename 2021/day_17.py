from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 17,
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
    _, _, x, y = inp_content.split(" ")
    x_min, x_max = x.split("..")
    y_min, y_max = y.split("..")
    return {
        "x_min": int(x_min[2:]),
        "y_min": int(y_min[2:]),
        "x_max": int(x_max.replace(",", "")),
        "y_max": int(y_max)
    }


def step(x, y, xv, yv):
    x += xv
    y += yv
    if xv > 0:
        xv -= 1
    elif x < 0:
        xv += 1
    yv -= 1
    return x, y, xv, yv


def shoot(d):
    y_max = 0
    combinations = set()
    yv_1, yv_2, xv_1, xv_2 = d["y_min"] - 1, abs(d["y_min"]), int(sqrt(2 * d["x_min"] + 0.25) - 0.5), d["x_max"] + 2
    for yv_ in range(yv_1, yv_2):
        for xv_ in range(xv_1, xv_2):
            yv = yv_
            xv = xv_
            x, y = 0, 0
            y_max_ = 0
            while y >= d["y_min"] and x <= d["x_max"]:
                x, y, xv, yv = step(x, y, xv, yv)
                if y > y_max_:
                    y_max_ = y
                if d["x_min"] <= x <= d["x_max"] and d["y_min"] <= y <= d["y_max"]:
                    y_max = y_max_
                    combinations.add((xv_, yv_))
                    break
    return y_max, len(combinations)

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    return shoot(inp)[0]  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)
    return shoot(inp)[1]


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
