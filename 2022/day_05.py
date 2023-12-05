from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 5,
    'year': 2022,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content
    # add further input processing here..
    stacks, steps = [e for e in inp_content.split("\n\n")]
    s = []
    for stack in reversed(stacks.split("\n")[:-1]):
        for i, l in enumerate(stack):
            if l in "[ ]":
                continue
            while True:
                try:
                    s[(i - 1) // 4].append(l)
                    break
                except IndexError:
                    s.append([])
    ss = []
    for step in steps.split("\n"):
        split_step = step.split(" ")
        ss.append((int(split_step[1]), int(split_step[3]), int(split_step[5])))
    return s, ss


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    stack, steps = parse_input(input_str)

    for step in steps:
        for _ in range(step[0]):
            stack[step[2] - 1].append(stack[step[1] - 1].pop())

    ans = "".join([s[-1] for s in stack])

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    stack, steps = parse_input(input_str)

    for step in steps:
        ns = []
        for _ in range(step[0]):
            ns.append(stack[step[1] - 1].pop())
        for _ in range(step[0]):
            stack[step[2] - 1].append(ns.pop())
    ans = "".join([s[-1] for s in stack])

    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
