from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 24,
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
    inp_content = [e.split(" ") for e in inp_content.split("\n")]
    return inp_content


def run(inp: list[list[str]], n: str) -> tuple[int, str]:
    d = defaultdict(int)
    c = 0
    accepted = ""
    print(f"{n = }")
    for ins, *l in inp:
        if ins == "inp":
            d[l[0]] = int(n[c])
            accepted += n[c]
            c += 1
        else:
            try:
                v = int(l[1])
            except ValueError:
                v = d[l[1]]
            if ins == "add":
                d[l[0]] = d[l[0]] + v
            elif ins == "mul":
                d[l[0]] = d[l[0]] * v
            elif ins == "div":
                if v == 0:
                    return -1, accepted
                x = d[l[0]] / v
                if x > 0:
                    d[l[0]] = floor(x)
                else:
                    d[l[0]] = ceil(x)
            elif ins == "mod":
                if v == 0:
                    return -1, accepted
                d[l[0]] = d[l[0]] % v
            elif ins == "eql":
                d[l[0]] = 1 if d[l[0]] == v else 0
    return d["z"], accepted


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    n = 99_999_999_999_999
    while n >= 11_111_111_111_111:
        x = str(n)
        if "0" in x:
            i = x.index("0")
            n = int(str(int(x[:i]) - 1) + "9" * (14 - i))
            continue
        r, s = run(inp, x)
        if r == 0:
            return int(n)
        n = int(s[:-1] + str(int(s[-1]) - 1) + "9" * (14 - len(s)))

    return None  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = None
    for ee in inp:
        pass

    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
