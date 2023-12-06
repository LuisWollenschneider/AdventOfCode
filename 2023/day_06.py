from utils import aoc_comm, create_test_file
import os
from typing import Optional

# --- update day/ year for each challenge
settings = {
    'day': 6,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
import re


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    mss = list(map(int, input_str.split('\n')[0].split(':')[1].strip().split()))
    ds = list(map(int, input_str.split('\n')[1].split(':')[1].strip().split()))

    res = 1
    for ms, d in zip(mss, ds):
        s = 0
        for i in range(1, ms):
            if i * (ms - i) > d:
                s += 1
        res *= s

    return res


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    ms = int(input_str.split('\n')[0].split(':')[1].replace(' ', ''))
    d = int(input_str.split('\n')[1].split(':')[1].replace(' ', ''))

    res = 0
    for i in range(1, ms):
        if i * (ms - i) > d:
            res += 1

    return res


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
