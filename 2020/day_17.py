from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 17,
    'year': 2020,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content, dims):
    inp_content = inp_content.strip()
    # add further input processing here...
    cubes = set((x, y) + (0,) * (dims - 2) for y, line in enumerate(inp_content.split("\n")) for x, c in enumerate(line) if c == "#")
    return cubes


def cycle(cubes, dims):
    new_cubes = set()

    def get_neighbours(cd):
        for ds in itertools.product((-1, 0, 1), repeat=dims):
            if all(d == 0 for d in ds):
                continue
            yield tuple(c + d for c, d in zip(cd, ds))

    tested_inactives = set()

    for coord in cubes:
        an = 0
        for n_coord in get_neighbours(coord):
            if n_coord in cubes:
                an += 1
                continue
            if n_coord in tested_inactives:
                continue
            tested_inactives.add(n_coord)
            active_neighbours = sum(nn_coord in cubes for nn_coord in get_neighbours(n_coord))
            if active_neighbours == 3:
                new_cubes.add(n_coord)

        if 2 <= an <= 3:
            new_cubes.add(coord)

    return new_cubes


def solve(inp, dims):
    cubes = parse_input(inp, dims)
    for _ in range(6):
        cubes = cycle(cubes, dims)
    return len(cubes)

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return solve(input_str, 3) # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    return solve(input_str, 4)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
