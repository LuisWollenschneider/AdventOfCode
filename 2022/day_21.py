from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 21,
    'year': 2022,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools

class Op:
    arg1 = None
    arg2 = None
    op = None
    res = None


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [e for e in inp_content.split("\n")]
    inp = {}
    for line in inp_content:
        o = Op()
        try:
            o.res = int(line.split(": ")[1].strip())
        except ValueError:
            o.op = line[11]
            o.arg1 = line[6:10]
            o.arg2 = line[13:17]
        inp[line.split(": ")[0]] = o
    return inp

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    ans = None
    for ee in inp:
        pass

    return ans  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def pre_compute(inp, ins):
    if ins == "humn":
        return None
    if inp[ins].res is not None:
        return inp[ins].res
    a = pre_compute(inp, inp[ins].arg1)
    b = pre_compute(inp, inp[ins].arg2)
    if a is None or b is None:
        return None
    res = 0
    if inp[ins].op == "+":
        res = a + b
    elif inp[ins].op == "*":
        res = a * b
    elif inp[ins].op == "-":
        res = a - b
    elif inp[ins].op == "/":
        res = a // b
    elif inp[ins].op == "=":
        res = 1 if a == b else 0
    inp[ins].res = res
    return res


def backtrace(inp, ins, res):
    if ins == "humn":
        return res
    a = inp[inp[ins].arg1].res
    b = inp[inp[ins].arg2].res
    if a is None:
        if inp[ins].op == "+":
            a = res - b
        elif inp[ins].op == "*":
            a = res // b
        elif inp[ins].op == "-":
            a = res + b
        elif inp[ins].op == "/":
            a = res * b
        elif inp[ins].op == "=":
            a = b if res == 1 else 0
        return backtrace(inp, inp[ins].arg1, a)
    elif b is None:
        if inp[ins].op == "+":
            b = res - a
        elif inp[ins].op == "*":
            b = res // a
        elif inp[ins].op == "-":
            b = a - res
        elif inp[ins].op == "/":
            b = a // res
        elif inp[ins].op == "=":
            b = a if res == 1 else 0
        return backtrace(inp, inp[ins].arg2, b)
    else:
        print("ERROR")
        exit(1)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    inp["root"].op = '='
    pre_compute(inp, "root")
    inp["humn"].res = None

    return backtrace(inp, "root", 1)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
