from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 14,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


d = {}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [e for e in inp_content.split("\n\n")]
    inp_content[1] = [y.split(" -> ") for y in inp_content[1].split("\n")]
    r1 = defaultdict(int)
    for i, l in enumerate(inp_content[0][:-1]):
        r1[l+inp_content[0][i+1]] += 1
    res = (
        r1,
        {x: y for x, y in inp_content[1]}
    )
    return res


def step(s: defaultdict[str, int]):
    res = defaultdict(int)
    for k, v in s.items():
        l = d[k]
        res[k[0]+l] += v
        res[l+k[1]] += v
    return res


def apply_polymer(input_str, n: int):
    global d
    inp, d = parse_input(input_str)
    for _ in range(n):
        inp = step(inp)

    c = defaultdict(int)
    for k, v in inp.items():
        c[k[0]] += v
        c[k[1]] += v
    c_ = Counter(c)
    max_value = c_.most_common()[0][1]
    min_value = max_value
    for v in c_.values():
        if min_value > v:
            min_value = v

    return max_value // 2 - min_value // 2 + 1

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return apply_polymer(input_str, 10)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    return apply_polymer(input_str, 40)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
