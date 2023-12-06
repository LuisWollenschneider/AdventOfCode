from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 8,
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
    inp_content = [e.split(" | ") for e in inp_content.split("\n")]
    return inp_content

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = 0
    for ee, eo in inp:
        for n in eo.split():
            if len(n) in [2, 3, 4, 7]:
                ans += 1

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = 0
    for ee, eo in inp:
        d = {}
        for n in ee.split():
            n: set = set(n)
            if len(n) == 2:
                d["1"] = n
            elif len(n) == 3:
                d["7"] = n
            elif len(n) == 4:
                d["4"] = n
            elif len(n) == 7:
                d["8"] = n
        for n in ee.split():
            n: set = set(n)
            if len(n) == 5:
                if d["1"].issubset(n):
                    d["3"] = n
            elif len(n) == 6:
                if not d["1"].issubset(n):
                    d["6"] = n
                elif not d["4"].issubset(n):
                    d["0"] = n
                else:
                    d["9"] = n
        for n in ee.split():
            n: set = set(n)
            if len(n) == 5:
                if d["1"].issubset(n):
                    pass
                elif n.issubset(d["6"]):
                    d["5"] = n
                else:
                    d["2"] = n
        out = ""
        for n in eo.split():
            n = set(n)
            for i, s in d.items():
                if n == s:
                    out += i
                    break
        ans += int(out)
    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
