from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 23,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import log10
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    connections = defaultdict(list)
    for e in inp_content.split("\n"):
        a, b = e.split("-")
        connections[b].append(a)
        connections[a].append(b)
    return connections


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    connections = parse_input(input_str)

    chief_nodes = [n for n in connections if n.startswith("t")]

    sets = set()
    for n in chief_nodes:
        for n1 in connections[n]:
            for n2 in connections[n]:
                if n1 == n2:
                    continue
                if n1 not in connections[n2]:
                    continue
                if n2 not in connections[n1]:
                    continue
                sets.add(tuple(sorted([n, n1, n2])))

    return len(sets)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[str]:
    connections = parse_input(input_str)

    largest = []
    for c in connections:
        rem_nodes = connections[c].copy()
        used_nodes = [c]

        while rem_nodes:
            n = rem_nodes.pop()
            if all(n in connections[un] for un in used_nodes):
                used_nodes.append(n)

        if len(used_nodes) > len(largest):
            largest = used_nodes

    return ",".join(sorted(largest))


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
