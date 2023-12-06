from utils_py import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day': 2,
    'year': 2019,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [int(e) for e in inp_content.split(",")]
    return inp_content


def add(a, b):
    return a + b


def mult(a, b):
    return a * b

    
@aoc_comm(settings, level=1)
def solve_l1(input_str, x1=12, x2=2):  # input data will be passed to this as string
    inp = parse_input(input_str)
    inp[1] = x1
    inp[2] = x2
    ans = None
    i = 0
    while True:
        if inp[i] == 99:
            return inp[0]
        if inp[i] == 1:
            func = add
        if inp[i] == 2:
            func = mult
        inp[inp[i+3]] = func(inp[inp[i+1]], inp[inp[i+2]])
        i += 4

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    ans = None
    for i in range(1_000_000):
        for j in range(1_000_000):
            try:
                res = solve_l1(input_str, j, i)
                if res == 19690720:
                    return 100 * j + i
            except:
                pass
        i += 1
    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
