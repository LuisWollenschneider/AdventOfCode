from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 7,
    'year': 2020,
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
    bags = {}
    for line in inp_content.split("\n"):
        bag, content = line.split(" bags contain ")
        bags[bag] = {}
        for c in content.replace(" bags", "").replace(" bag", "").replace(".", "").split(", "):
            n, b = c.split(" ", 1)
            if n == "no":
                continue
            bags[bag][b] = int(n)
    return bags


def contains_shiny_gold(bag, bags):
    if "shiny gold" in bags[bag]:
        return 1
    for b in bags[bag]:
        if contains_shiny_gold(b, bags):
            return 1
    return 0


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    bags = parse_input(input_str)
    ans = 0
    for bag in bags:
        ans += contains_shiny_gold(bag, bags)
    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def count_bags_inside(bag, bags):
    t = 0
    for b, n in bags[bag].items():
        t += n * (1 + count_bags_inside(b, bags))
    return t


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    bags = parse_input(input_str)

    return count_bags_inside("shiny gold", bags)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
