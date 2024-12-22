from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 22,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import log10
import functools
import itertools
from tqdm import tqdm


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp = [int(e) for e in inp_content.split("\n")]
    return inp


def mix(n, s):
    return n ^ s


def prune(n):
    return n % 16777216


def next_secret(n):
    n = prune(mix(n << 6, n))
    n = prune(mix(n >> 5, n))
    n = prune(mix(n << 11, n))
    return n


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    secrets = parse_input(input_str)

    r = 0
    for s in secrets:
        for _ in range(2000):
            s = next_secret(s)
        r += s
    return r


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    secrets = parse_input(input_str)

    total_changes = defaultdict(int)
    for s in secrets:
        changes = {}
        a, b, c, d, e = None, None, None, None, None
        for _ in range(2000):
            s = next_secret(s)
            a, b, c, d, e = b, c, d, e, s % 10
            if a is None or b is None or c is None or d is None:
                continue
            c1, c2, c3, c4 = b - a, c - b, d - c, e - d
            if (c1, c2, c3, c4) not in changes:
                changes[(c1, c2, c3, c4)] = e
                total_changes[(c1, c2, c3, c4)] += e

    max_change = max(total_changes, key=lambda x: total_changes[x])

    return total_changes[max_change]


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
