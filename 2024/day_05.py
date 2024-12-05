from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 5,
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
    rules, updates = inp_content.split("\n\n")

    rules = [list(map(int, e.split("|"))) for e in rules.split("\n")]
    updates = [list(map(int, e.split(","))) for e in updates.split("\n")]

    return rules, updates


def is_valid(u, rules):
    for r1, r2 in rules:
        try:
            if u.index(r1) > u.index(r2):
                return False
        except ValueError:
            continue
    return True


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    rules, updates = parse_input(input_str)

    s = 0
    for u in updates:
        if is_valid(u, rules):
            s += u[len(u) // 2]

    return s


def build_update(update: list[int], remaining_numbers: list[int], rules: list):
    if not remaining_numbers:
        if is_valid(update, rules):
            return update
        return None

    x = remaining_numbers.pop(0)

    min_index = 0
    max_index = len(update)

    for r1, r2 in rules:
        if r1 != x and r2 != x:
            continue

        if r1 in update:
            min_index = max(min_index, update.index(r1) + 1)
        elif r2 in update:
            max_index = min(max_index, update.index(r2))

    for i in range(min_index, max_index + 1):
        new_update = update.copy()
        new_update.insert(i, x)

        u = build_update(new_update, remaining_numbers, rules)

        if u:
            return u

    return None


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    rules, updates = parse_input(input_str)

    invalid_updates = list(filter(lambda x: not is_valid(x, rules), updates))

    s = 0
    for u in invalid_updates:
        new_u = build_update([u[0]], u[1:], rules)

        s += new_u[len(new_u) // 2]

    return s


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
