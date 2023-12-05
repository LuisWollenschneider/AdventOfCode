from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 25,
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
    inp_content = [e for e in inp_content.split("\n")]
    return inp_content


def convert_to_int(s):
    n = 0
    for c in s:
        n *= 5
        if c == '=':
            n -= 2
        elif c == '-':
            n -= 1
        else:
            n += int(c)
    return n


def convert_to_str(n):
    s = ""
    pow5 = 1
    while n > 0:
        for i in range(-2, 3):
            if (n - (i * 5**(pow5-1))) % 5 ** pow5 == 0:
                if i == -2:
                    s += '='
                elif i == -1:
                    s += '-'
                else:
                    s += str(i)
                n -= i * 5**(pow5-1)
                break
        pow5 += 1
    return s[::-1]

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = 0
    for ee in inp:
        ans += convert_to_int(ee)

    return convert_to_str(ans)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


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
