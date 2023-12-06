from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 6,
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
    inp_content = [int(e) for e in inp_content.split(",")]
    return inp_content


def lanternfish(days, inp):
    fish = {}
    for f in inp:
        if f not in fish:
            fish[f] = 0
        fish[f] += 1
    for i in range(days):
        fish_ = {}
        for f, n in fish.items():
            if f == 0:
                if 6 not in fish_:
                    fish_[6] = 0
                fish_[6] += n
                fish_[8] = n
            else:
                if f-1 not in fish_:
                    fish_[f-1] = 0
                fish_[f-1] += n
        fish = fish_

    return sum(fish.values())

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    return lanternfish(80, inp)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)
    return lanternfish(256, inp)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
