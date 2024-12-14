from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 13,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


class Prize:
    def __init__(self, A, B, P):
        self.A: list[int, int] = A
        self.B: list[int, int] = B
        self.P: list[int, int] = P

    def solve(self, most=True):
        """

        a * AX + b * BX = PX
        a * AY + b * BY = PY

        AX BX | PX
        AY BY | PY

        AX BX | PX   * lcm(AX, AY) / AX
        AY BY | PY   * lcm(AX, AY) / AY

        II - I
        mAX mBX | mPX
         0  nBY | nPY
        """
        d = gcd(self.A[0], self.B[0], self.A[1], self.B[1], self.P[0], self.P[1])
        self.A = [e // d for e in self.A]
        self.B = [e // d for e in self.B]
        self.P = [e // d for e in self.P]

        m = lcm(self.A[0], self.A[1])
        m1 = m // self.A[0]
        self.A[0] *= m1
        self.B[0] *= m1
        self.P[0] *= m1

        m2 = m // self.A[1]
        self.A[1] = self.A[1] * m2 - self.A[0]
        self.B[1] = self.B[1] * m2 - self.B[0]
        self.P[1] = self.P[1] * m2 - self.P[0]

        assert self.A[1] == 0

        if self.P[1] % self.B[1] != 0:
            return 0

        b = self.P[1] // self.B[1]
        if most:
            b = min(b, 100)

        if (self.P[0] - b * self.B[0]) % self.A[0] != 0:
            return 0

        a = (self.P[0] - b * self.B[0]) // self.A[0]
        if a < 0:
            return 0

        if most and a > 100:
            return 0

        return a * 3 + b


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..

    prizes = []

    def parse_point(p, s):
        x, y = p.split(", ")
        x = int(x[x.find(s)+1:])
        y = int(y[y.find(s)+1:])
        return [x, y]

    for prize in inp_content.split("\n\n"):
        A, B, P = prize.split("\n")
        prizes.append(Prize(
            parse_point(A, "+"),
            parse_point(B, "+"),
            parse_point(P, "=")
        ))

    return prizes


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    prizes = parse_input(input_str)

    return sum(p.solve() for p in prizes)


@aoc_comm(settings, level=2, test_case=False)
def solve_l2(input_str) -> Optional[int]:
    prizes = parse_input(input_str)
    for p in prizes:
        p.P = [e + 10000000000000 for e in p.P]

    return sum(p.solve(False) for p in prizes)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
