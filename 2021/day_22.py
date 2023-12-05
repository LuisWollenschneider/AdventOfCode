from utils import aoc_comm, create_test_file
import os
from typing import Optional, Any
import re

# --- update day/ year for each challenge
settings = {
    'day': 22,
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
    res = []
    for e in inp_content.split("\n"):
        state, x, y, z = e.split("=")
        state = state.split(" ")[0]
        x = x.split(",")[0]
        y = y.split(",")[0]
        z = z.split(",")[0]
        x1, x2 = map(int, x.split(".."))
        y1, y2 = map(int, y.split(".."))
        z1, z2 = map(int, z.split(".."))
        res.append((state, x1, x2, y1, y2, z1, z2))
    return res


def get_set(x_min, x_max, y_min, y_max, z_min, z_max, lim_min, lim_max):
    res = set()
    for x in range(max(x_min, lim_min), min(x_max, lim_max) + 1):
        for y in range(max(y_min, lim_min), min(y_max, lim_max) + 1):
            for z in range(max(z_min, lim_min), min(z_max, lim_max) + 1):
                res.add((x, y, z))
    return res


class Range:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.ranges = []

    def remove(self, r):
        if self.ranges:
            for r_ in self.ranges:
                r_.remove(r)
            return
        if self.included(r):
            return
        if not self.overlap(r):
            return
        nx_min = max(r.x_max + 1, self.x_min)
        nx_max = min(r.x_min - 1, self.x_max)
        ny_min = max(r.y_max + 1, self.y_min)
        ny_max = min(r.y_min - 1, self.y_max)
        self.ranges = [
            # Sides
            Range(self.x_min, nx_max, max(self.y_min, r.y_min), min(self.y_max, r.y_max), max(self.z_min, r.z_min), min(self.z_max, r.z_max)),
            Range(nx_min, self.x_max, max(self.y_min, r.y_min), min(self.y_max, r.y_max), max(self.z_min, r.z_min), min(self.z_max, r.z_max)),
            Range(max(self.x_min, r.x_min), min(self.x_max, r.x_max), self.y_min, ny_max, max(self.z_min, r.z_min), min(self.z_max, r.z_max)),
            Range(max(self.x_min, r.x_min), min(self.x_max, r.x_max), ny_min, self.y_max, max(self.z_min, r.z_min), min(self.z_max, r.z_max)),
            Range(max(self.x_min, r.x_min), min(self.x_max, r.x_max), max(self.y_min, r.y_min), min(self.y_max, r.y_max), self.z_min, min(r.z_min - 1, self.z_max)),
            Range(max(self.x_min, r.x_min), min(self.x_max, r.x_max), max(self.y_min, r.y_min), min(self.y_max, r.y_max), max(r.z_max + 1, self.z_min), self.z_max),
            # Corners
            Range(self.x_min, r.x_min - 1, self.y_min, r.y_min - 1, self.z_min, r.z_min - 1),
            Range(r.x_max + 1, self.x_max, self.y_min, r.y_min - 1, self.z_min, r.z_min - 1),
            Range(self.x_min, r.x_min - 1, r.y_max + 1, self.y_max, self.z_min, r.z_min - 1),
            Range(self.x_min, r.x_min - 1, self.y_min, r.y_min - 1, r.z_max + 1, self.z_max),
            Range(r.x_max + 1, self.x_max, r.y_max + 1, self.y_max, self.z_min, r.z_min - 1),
            Range(r.x_max + 1, self.x_max, self.y_min, r.y_min - 1, r.z_max + 1, self.z_max),
            Range(self.x_min, r.x_min - 1, r.y_max + 1, self.y_max, r.z_max + 1, self.z_max),
            Range(r.x_max + 1, self.x_max, r.y_max + 1, self.y_max, r.z_max + 1, self.z_max),
            # Edges (12)
            # Range(r.x_max, self.x_max, self.y_min, r.y_min, max(r.z_max + 1, self.z_min), min(r.z_min - 1, self.z_max)),
            # Range(self.x_min, self.x_max, self.y_min, r.y_min - 1, self.z_min, r.z_min - 1),
        ]
        self.x_min = self.x_max + 1

    def overlap(self, r) -> bool:
        if self.y_min <= r.y_min <= self.y_max or self.y_min <= r.y_max <= self.y_max:
            if self.x_min <= r.x_min <= self.x_max or self.x_min <= r.x_max <= self.x_max:
                return True
            if self.z_min <= r.z_min <= self.z_max or self.z_min <= r.z_max <= self.z_max:
                return True
        if self.x_min <= r.x_min <= self.x_max or self.x_min <= r.x_max <= self.x_max:
            if self.z_min <= r.z_min <= self.z_max or self.z_min <= r.z_max <= self.z_max:
                return True
        return False

    def included(self, r) -> bool:
        if self.x_min < r.x_min: return False
        if self.x_max > r.x_max: return False
        if self.y_min < r.y_min: return False
        if self.y_max < r.y_max: return False
        if self.z_min < r.z_min: return False
        if self.z_max < r.z_max: return False
        self.x_min = self.x_max + 1
        return True

    def x_range(self):
        return self.x_max - self.x_min + 1

    def y_range(self):
        return self.y_max - self.y_min + 1

    def z_range(self):
        return self.z_max - self.z_min + 1

    def length(self):
        if self.ranges:
            return sum([r.length() for r in self.ranges])
        return self.x_range() * self.y_range() * self.z_range()

    def overwrite(self, r):
        self.x_min = r.x_min
        self.x_max = r.x_max
        self.y_min = r.y_min
        self.y_max = r.y_max
        self.y_min = r.y_min
        self.y_max = r.y_max
        self.ranges = r.ranges

    def __bool__(self):
        self.ranges = list(filter(bool, self.ranges))
        if len(self.ranges) == 1:
            self.overwrite(self.ranges[0])
        if self.ranges:
            return True
        if self.x_min > self.x_max: return False
        if self.y_min > self.y_max: return False
        if self.z_min > self.z_max: return False
        return True

    def __str__(self):
        return f"x={self.x_min}..{self.x_max},y={self.y_min}..{self.y_max},z={self.z_min}..{self.z_max}"


def efficiency(inp) -> int:
    ranges: list[Range] = []
    for state, x_min, x_max, y_min, y_max, z_min, z_max in inp:
        r: Range = Range(max(x_min, -50), min(x_max, 50), max(y_min, -50), min(y_max, 50), max(z_min, -50), min(z_max, 50))
        if not r:
            continue
        for r_ in ranges:
            r_.remove(r)
        if state == "on":
            ranges.append(r)
        ranges = list(filter(bool, ranges))
        print(sum([r.length() for r in ranges]))
    return sum([r.length() for r in ranges])


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)

    return efficiency(inp)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation
    res = set()
    for state, x_min, x_max, y_min, y_max, z_min, z_max in inp:
        s = get_set(x_min, x_max, y_min, y_max, z_min, z_max, -50, 50)
        if state == "on":
            res = res.union(s)
        else:
            res = res - s
        print(len(res))
    return len(res)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = parse_input(input_str)

    ans = None
    for ee in inp:
        pass

    return ans


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
