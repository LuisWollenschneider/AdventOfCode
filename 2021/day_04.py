from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 4,
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
    return inp_content[0].split(","), [el.replace("\n", " ").split() for el in inp_content[1:]]


def check(field: list[str]) -> bool:
    for i in range(5):
        if field[i::5].count("-1") == 5:
            return True
    for i in range(5):
        if field[i * 5:(i + 1) * 5].count("-1") == 5:
            return True
    if [field[0], field[6], field[12], field[18], field[24]].count("-1") == 5:
        return True
    if [field[4], field[8], field[12], field[16], field[20]].count("-1") == 5:
        return True
    return False

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp1, inp2 = parse_input(input_str)

    ans = None
    for n in inp1:
        for x in inp2:
            if n not in x:
                continue
            x[x.index(n)] = "-1"
            if check(x):
                return (sum([int(el) for el in x if el != "-1"])) * int(n)
    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp1, inp2 = parse_input(input_str)

    ans = None
    for n in inp1:
        inp2_ = inp2.copy()
        c = 0
        for i, x in enumerate(inp2_):
            if n not in x:
                continue
            x[x.index(n)] = "-1"
            if check(x):
                ans = inp2.pop(i - c), int(n)
                c += 1
    return (sum([int(el) for el in ans[0] if el != "-1"])) * int(ans[1])


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
