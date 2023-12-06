from utils_py import aoc_comm
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 10,
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
    inp_content = [e for e in inp_content.split("\n")]
    return inp_content

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = None
    complement = {")": "(", "]": "[", "}": "{", ">": "<"}
    errors = {")": 0, "]": 0, "}": 0, ">": 0}
    for ee in inp:
        stack = []
        for e in ee:
            if e in "([{<":
                stack.append(e)
            else:
                if not stack:
                    errors[e] += 1
                    break
                if stack[-1] == complement[e]:
                    stack.pop()
                else:
                    errors[e] += 1
                    break

    return 3 * errors[")"] + 57 * errors["]"] + 1197 * errors["}"] + 25137 * errors[">"]  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = None
    complement = {")": "(", "]": "[", "}": "{", ">": "<"}
    complement2 = {"(": ")", "[": "]", "{": "}", "<": ">"}
    errors = {")": 1, "]": 2, "}": 3, ">": 4}
    lines = inp.copy()
    for ee in inp:
        stack = []
        for e in ee:
            if e in "([{<":
                stack.append(e)
            else:
                if not stack:
                    lines.remove(ee)
                    break
                if stack[-1] == complement[e]:
                    stack.pop()
                else:
                    lines.remove(ee)
                    break
    scores = []
    for ee in lines:
        stack = []
        for e in ee:
            if e in "([{<":
                stack.append(e)
            else:
                if stack[-1] == complement[e]:
                    stack.pop()
        score = 0
        while stack:
            score = score * 5 + errors[complement2[stack[-1]]]
            stack.pop()
        scores.append(score)
    scores.sort()
    print(scores)
    return scores[int(len(scores) / 2)]


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
