from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 9,
    'year': 2024,
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
    inp = [int(e) for e in inp_content]

    return inp


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    i, j = 0, len(inp)
    j = j - 1 if j % 2 != 0 else j
    s = 0
    idx = 0
    while i <= j:
        if i % 2 == 0:
            for x in range(inp[i]):
                s += idx * i // 2
                idx += 1
        else:
            for x in range(inp[i]):
                while inp[j] == 0:
                    j -= 2
                s += idx * j // 2
                idx += 1
                inp[j] -= 1
        i += 1

    return s


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    spaces = []
    files = []
    idx = 0
    for i, f in enumerate(inp):
        if i % 2 == 0:
            files.append((idx, f, i))
        else:
            spaces.append((idx, f))
        idx += f

    final_files = []
    for idx, f, i in files[::-1]:
        for si, s in enumerate(spaces):
            sidx, sf = s
            if sidx > idx:
                final_files.append((idx, f, i))
                break
            if sf < f:
                continue
            spaces[si] = (sidx + f, sf - f)
            final_files.append((sidx, f, i))
            break
        else:
            final_files.append((idx, f, i))

    s = 0
    for idx, f, i in final_files:
        for x in range(f):
            s += idx * i // 2
            idx += 1
    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
