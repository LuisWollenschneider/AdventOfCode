from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 16,
    'year': 2022,
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
    inp_content = [e.split() for e in inp_content.split("\n")]
    inp = []
    # [(0, 'Valve'), (1, 'AA'), (2, 'has'), (3, 'flow'), (4, 'rate=0;'), (5, 'tunnels'),
    # (6, 'lead'), (7, 'to'), (8, 'valves'), (9, 'DD,'), (10, 'II,'), (11, 'BB')]
    d1 = {}
    d2 = {}
    for el in inp_content:
        d1[el[1]] = int(el[4][5:-1])
        d2[el[1]] = [e.replace(",", "") for e in el[9:]]
    d3 = {}

    l = [el for el, v in d1.items() if v > 0]
    t = {e: 2 ** i for i, e in enumerate(l)}
    t["AA"] = 0

    def dist(init, key, visited) -> list[tuple[str, int]]:
        #  to find a key with d1[key] > 0
        if d1[key] > 0 and key != init:
            return [(key, 0)]
        if key in d3:
            return [(k_, l_) for k_, l_ in d3[key] if k_ != init]
        a = {}
        for e in d2[key]:
            if e in visited:
                continue
            visited.append(e)
            for k_, l_ in dist(init, e, visited):
                if k_ in a:
                    a[k_] = min(a[k_], l_ + 1)
                else:
                    a[k_] = l_ + 1
            visited.pop()
        return [(k_, l_) for k_, l_ in a.items()]

    for k, v in d2.items():
        d3[k] = dist(k, k, [k])
    return t, d1, d3


mem = {}
valves = 0


def traverse(tr: dict, d1: dict, d2: dict, start: str, opened: int, minutes, other=0) -> int:
    K = (((((opened << 16) + tr[start]) << 6) + minutes) << 1) + other
    if K in mem:
        return mem[K]
    if not opened ^ valves:
        return 0
    if minutes <= 1:
        if other == 0:
            return 0
        return traverse(tr, d1, d2, "AA", opened, 26)
    m = 0
    for e, t in d2[start]:
        m = max(m, traverse(tr, d1, d2, e, opened, minutes - t, other))
    if d1[start] > 0 and not tr[start] & opened:
        mins = minutes - 1
        m = max(m, d1[start] * mins + traverse(tr, d1, d2, start, opened | tr[start], mins, other))
    mem[K] = m
    return m


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    global valves, mem
    t, d1, d2 = parse_input(input_str)

    mem = {}
    valves = sum(t.values())
    return traverse(t, d1, d2, "AA", 0, 30)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    global valves, mem
    t, d1, d2 = parse_input(input_str)

    mem = {}
    valves = len([e for e in d1.keys() if d1[e] > 0])
    return traverse(t, d1, d2, "AA", 0, 26, 1)
    # return traverse_sim(d1, d2, "AA", "AA", [], 26, 26, {})


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
