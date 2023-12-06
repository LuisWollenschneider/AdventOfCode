from utils_py import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day': 3,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content: str) -> list[str]:
    inp_content = inp_content.strip()
    inp_content = [e for e in inp_content.split("\n")]
    return inp_content

    
@aoc_comm(settings, level=1)
def solve_l1(input_str: str) -> int:
    inp: list[str] = parse_input(input_str)
    joint: str = input_str.replace("\n", "")
    ans = int(''.join(["0" if joint[i::len(inp[0])].count("0") > len(inp) / 2 else "1" for i in range(len(inp[0]))]), 2)
    return ans * (ans ^ int("1" * len(inp[0]), 2))


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> int:
    inp = parse_input(input_str)

    def comp1(a: str, b: str) -> bool:
        return a != b

    def comp2(a: str, b: str) -> bool:
        return a == b

    def get_val(inp_: list[str], comp) -> int:
        for i in range(len(inp_[0])):
            if len(inp_) == 1:
                break
            c = 0
            for ee in inp_:
                c += 1 if ee[i] == "0" else -1
            b: str = "0" if c > 0 else "1"
            inp_ = [x for x in inp_ if comp(x[i], b)]
        return int(inp_[0], 2)
    return get_val(inp.copy(), comp1) * get_val(inp.copy(), comp2)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
