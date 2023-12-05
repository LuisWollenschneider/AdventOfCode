from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 16,
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
    return bin(int(inp_content, 16)).replace("0b", "").zfill(len(inp_content) * 4)


def parse_packet(inp, p=0) -> tuple[int, int, int]:
    versions = int(inp[p:p + 3], 2)
    type_id = int(inp[p + 3:p + 6], 2)
    p += 6
    n = 0
    if type_id == 4:
        n = ""
        while inp[p] != "0":
            n += inp[p + 1:p + 5]
            p += 5
        n += inp[p + 1:p + 5]
        p += 5
        n = int(n, 2)
    else:
        ns = []
        if inp[p] == "0":
            length = int(inp[p + 1:p + 16], 2)
            p += 16
            v_, ns = parse(inp[p:], length)
            versions += v_
            p += length
        else:
            packets = int(inp[p + 1:p + 12], 2)
            p += 12
            for i in range(packets):
                p_, v_, n_ = parse_packet(inp[p:])
                ns.append(n_)
                p += p_
                versions += v_
        if type_id == 0:
            n = sum(ns)
        elif type_id == 1:
            n = 1
            for n_ in ns:
                n *= n_
        elif type_id == 2:
            n = min(ns)
        elif type_id == 3:
            n = max(ns)
        elif type_id == 5:
            n = 1 if ns[0] > ns[1] else 0
        elif type_id == 6:
            n = 1 if ns[0] < ns[1] else 0
        elif type_id == 7:
            n = 1 if ns[0] == ns[1] else 0
    return p, versions, n


def parse(inp, l, p=0) -> tuple[int, list]:
    versions = 0
    ns = []
    while p < l:
        if inp[p:].count("1") == 0:
            return versions, ns
        p_, v_, n = parse_packet(inp[p:])
        ns.append(n)
        p += p_
        versions += v_
    return versions, ns

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    p, v, n = parse_packet(inp)

    return v  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)
    p, v, n = parse_packet(inp)

    return n


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
