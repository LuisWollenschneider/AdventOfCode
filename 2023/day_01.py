from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 1,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def get_first_digit(inp):
    for i in range(len(inp)):
        if inp[i].isdigit():
            return inp[i]
        for d, s in zip("123456789", ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]):
            if inp[i:].startswith(s):
                return d
    raise ValueError("No digit found")


def get_last_digit(inp):
    for i in range(len(inp) - 1, -1, -1):
        if inp[i].isdigit():
            return inp[i]
        for d, s in zip("123456789", ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]):
            if inp[i:].startswith(s):
                return d
    raise ValueError("No digit found")


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = []
    for line in input_str.splitlines():
        inp.append("".join(c for c in line if c in "0123456789"))

    s = 0
    for el in inp:
        try:
            s += int(el[0] + el[-1])
        except IndexError:
            pass
    return s
    # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = input_str.splitlines()

    s = 0
    for el in inp:
        try:
            s += int(get_first_digit(el) + get_last_digit(el))
        except IndexError:
            pass
    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
