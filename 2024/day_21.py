from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 21,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
from tqdm import tqdm


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    inp = inp_content.split("\n")
    return inp


keypad_1 = [
    "789",
    "456",
    "123",
    " 0A"
]

keypad_2 = [
    " ^A",
    "<v>"
]


def from_to_in_dir(start: tuple[int, int], end: tuple[int, int]):
    """
    WTF, why is the order this important???

    Time wasted searching for bugs outside this function:
                8 hours

    Time wasted shuffling the order of directions:
                1 hours
    """
    s = ""
    s += "<" * max(start[0] - end[0], 0)
    s += "^" * max(start[1] - end[1], 0)
    s += "v" * max(end[1] - start[1], 0)
    s += ">" * max(end[0] - start[0], 0)
    return s


def crosses_space(pos, dirs, space):
    for d in dirs:
        if d == "^":
            pos = (pos[0], pos[1] - 1)
        elif d == "v":
            pos = (pos[0], pos[1] + 1)
        elif d == "<":
            pos = (pos[0] - 1, pos[1])
        elif d == ">":
            pos = (pos[0] + 1, pos[1])
        if pos == space:
            return True
    return False


def build_keypad_paths(keypad):
    key_to_pos = {}
    space = None
    for y, line in enumerate(keypad):
        for x, c in enumerate(line):
            if c == " ":
                space = (x, y)
                continue
            key_to_pos[c] = (x, y)

    paths = {}
    for key, pos in key_to_pos.items():
        for key2, pos2 in key_to_pos.items():
            paths[key, key2] = from_to_in_dir(pos, pos2)

            if crosses_space(pos, paths[key, key2], space):
                # print(f"Reversed {key} -> {key2} ({paths[key, key2]} - {paths[key, key2][::-1]})")
                paths[key, key2] = paths[key, key2][::-1]

    return paths


def replace_instructions(start, target, keypad_paths):
    return keypad_paths[start, target] + "A"


def instructions(inst, keypad_paths):
    new_inst = ""
    start = "A"
    for c in inst:
        new_inst += replace_instructions(start, c, keypad_paths)
        start = c
    return new_inst


@functools.cache
def robot_instructions(fr, to, robots):
    if robots == 0:
        return 1

    inst = replace_instructions(fr, to, ROBOT_PATHS)
    s = 0
    for i1, i2 in zip("A" + inst, inst):
        s += robot_instructions(i1, i2, robots - 1)
    return s


# Don't like global objects for aoc, but I couldn't be bothered to implement it properly after 8 hours of debugging the
# wrong piece of code
ROBOT_PATHS = ...


def solve(input_str, robots):
    global ROBOT_PATHS
    codes = parse_input(input_str)
    keypad_paths = build_keypad_paths(keypad_1)
    robot_keypad_paths = build_keypad_paths(keypad_2)
    ROBOT_PATHS = robot_keypad_paths

    s = 0
    for c, original_code in enumerate(codes):
        code = instructions(original_code, keypad_paths)
        a = 0
        for i1, i2 in zip("A" + code, code):
            a += robot_instructions(i1, i2, robots)
        s += a * int(original_code[:-1])

    return s


@aoc_comm(settings, level=1, previous_attempts=[212830])
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return solve(input_str, 2)


@aoc_comm(settings, level=2, test_case=False, previous_attempts=[
    374956388679302,
    405054112481204,    # I know this looks desperate...
    287046661958274,
    295271598127906,    # shuffling the `from_to_in_dir()` function results in
    308172507493178,    # these incorrect answers
    414448905467796
])
def solve_l2(input_str) -> Optional[int]:
    return solve(input_str, 25)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
