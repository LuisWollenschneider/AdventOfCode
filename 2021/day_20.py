from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 20,
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
    inp_content = [e for e in inp_content.split("\n\n")]
    return inp_content[0], inp_content[1].split("\n")


def get_surrounding_int(img: list[str], x: int, y: int, base_char: str) -> int:
    bin_str = ""
    for i in [-1, 0, 1]:
        if 0 <= x + i < len(img):
            for j in [-1, 0, 1]:
                if 0 <= y + j < len(img[0]):
                    bin_str += img[x+i][y+j]
                else:
                    bin_str += base_char
        else:
            bin_str += base_char * 3
    return int(bin_str.replace(".", "0").replace("#", "1"), 2)


def step(img: list[str], base_char: str, reference: str) -> tuple[list[str], str]:
    res = []
    for i in range(-1, len(img) + 1):
        res.append("")
        for j in range(-1, len(img[0]) + 1):
            res[-1] += reference[get_surrounding_int(img, i, j, base_char)]
    base_char = reference[int((base_char * 9).replace(".", "0").replace("#", "1"), 2)]
    return res, base_char


def count_pxl(img: list[str], char: str = "#") -> int:
    res = 0
    for l in img:
        res += l.count(char)
    return res


def run(input_str, n=2):
    reference, img = parse_input(input_str)
    base_char = "."
    for i in range(n):
        img, base_char = step(img, base_char, reference)

    return count_pxl(img)


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    return run(input_str)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    return run(input_str, 50)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
