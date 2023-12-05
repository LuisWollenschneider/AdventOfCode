from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 20,
    'year': 2022,
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
    inp_content = [int(e) for e in inp_content.split("\n")]
    return inp_content


def shuffle(x, y):
    for t in x:
        idx = y.index(t)
        y.pop(idx)
        new_idx = (idx + t[0]) % len(y)
        if new_idx == 0 and idx != 0:
            new_idx = len(x) - 1
        y.insert(new_idx, t)
    return y


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    zero = inp.index(0)
    x = [(el, i) for i, el in enumerate(inp)]
    y = x.copy()
    y = shuffle(x, y)

    ans = 0
    zero_idx = y.index((0, zero))
    for i in [1000, 2000, 3000]:
        ans += y[(zero_idx + i) % len(inp)][0]

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    zero = inp.index(0)
    x = [(el * 811589153, i) for i, el in enumerate(inp)]
    y = x.copy()
    for i in range(10):
        y = shuffle(x, y)

    ans = 0
    zero_idx = y.index((0, zero))
    for i in [1000, 2000, 3000]:
        ans += y[(zero_idx + i) % len(inp)][0]

    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
