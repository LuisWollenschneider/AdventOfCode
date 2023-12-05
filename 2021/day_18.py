from copy import copy
from mimetypes import init

from utils import aoc_comm, create_test_file
import os
from typing import Optional, Union
import re

# --- update day/ year for each challenge
settings = {
    'day': 18,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


class SnailfishNumber:
    left = None
    right = None
    parent = None

    def __init__(self, left=None, right=None, parent=None):
        self.left = left
        self.right = right
        self.parent = parent

    def parse(self, inp: str):
        if inp[0] != "[":
            raise ValueError
        if inp[1] == "[":
            self.left = SnailfishNumber(parent=self)
            inp = self.left.parse(inp[1:])
        else:
            self.left = int(inp[1])
        i = inp.index(",")
        if inp[i+1] == "[":
            self.right = SnailfishNumber(parent=self)
            inp = self.right.parse(inp[i+1:])
        else:
            self.right = int(inp[i+1])
            inp = inp[i+2:]
        if inp[0] != "]":
            raise ValueError
        return inp[1:]

    def magnitude(self):
        res = 0
        if isinstance(self.left, int):
            res += self.left * 3
        else:
            res += self.left.magnitude() * 3
        if isinstance(self.right, int):
            res += self.right * 2
        else:
            res += self.right.magnitude() * 2
        return res

    def is_primary(self):
        return isinstance(self.left, int) and isinstance(self.right, int)

    def depth(self):
        ld = self.left.depth() if isinstance(self.left, SnailfishNumber) else 0
        rd = self.right.depth() if isinstance(self.right, SnailfishNumber) else 0
        return max(ld, rd) + 1

    def find_right(self, n, sn):
        if self.right is sn:
            if self.parent is None:
                return
            self.parent.find_right(n, self)
            return
        if isinstance(self.right, SnailfishNumber):
            self.right.find_most_left(n)
            return
        self.right += n

    def find_most_left(self, n):
        if isinstance(self.left, SnailfishNumber):
            self.left.find_most_left(n)
            return
        self.left += n

    def find_left(self, n, sn):
        if self.left is sn:
            if self.parent is None:
                return
            self.parent.find_left(n, self)
            return
        if isinstance(self.left, SnailfishNumber):
            self.left.find_most_right(n)
            return
        self.left += n

    def find_most_right(self, n):
        if isinstance(self.right, SnailfishNumber):
            self.right.find_most_right(n)
            return
        self.right += n

    def explode(self, n):
        if isinstance(self.left, SnailfishNumber):
            if n >= 3 and self.left.is_primary():
                l = self.left.left
                r = self.left.right
                self.find_right(r, self.left)
                self.find_left(l, self.left)
                self.left = 0
                return True
            else:
                if self.left.explode(n + 1):
                    return True
        if isinstance(self.right, SnailfishNumber):
            if n >= 3 and self.right.is_primary():
                l = self.right.left
                r = self.right.right
                self.find_left(l, self.right)
                self.find_right(r, self.right)
                self.right = 0
                return True
            else:
                if self.right.explode(n + 1):
                    return True
        return False

    def split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                t = self.left / 2
                self.left = SnailfishNumber(parent=self)
                self.left.left = int(t)
                self.left.right = ceil(t)
                return True
        else:
            if self.left.split():
                return True
        if isinstance(self.right, int):
            if self.right >= 10:
                t = self.right / 2
                self.right = SnailfishNumber(parent=self)
                self.right.left = int(t)
                self.right.right = ceil(t)
                return True
        else:
            if self.right.split():
                return True
        return False

    def reduce(self):
        a = True
        while a:
            a = False
            if self.explode(0):
                a = True
                continue
            if self.split():
                a = True

    def __str__(self):
        return f"[{self.left},{self.right}]"


def parse_input(inp_content):
    inp_content = inp_content.strip().split("\n")
    # add further input processing here..

    sns = []
    for inp in inp_content:
        sn = SnailfishNumber()
        sn.parse(inp)
        sns.append(sn)

    return sns

    
@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    sns = parse_input(input_str)

    res = sns[0]
    for sn in sns[1:]:
        temp = SnailfishNumber(res, sn)
        res.parent = temp
        sn.parent = temp
        temp.reduce()
        res = temp
    return res.magnitude()  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    sns = parse_input(input_str)

    res = 0
    for sn1 in sns:
        for sn2 in sns:
            if sn1 is sn2:
                continue
            sn1_, sn2_ = SnailfishNumber(), SnailfishNumber()
            sn1_.parse(str(sn1))
            sn2_.parse(str(sn2))
            sn = SnailfishNumber(sn1_, sn2_)
            sn1_.parent = sn
            sn2_.parent = sn
            sn.reduce()
            m = sn.magnitude()
            if m > res:
                res = m

    return res


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
