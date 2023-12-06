from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 19,
    'year': 2021,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


def parse_input(inp_content) -> list[set[tuple[int, int, int]]]:
    inp_content = inp_content.strip()
    # add further input processing here..
    inp_content = [set([tuple(map(int, p.split(","))) for p in e.split("\n")[1:]]) for e in inp_content.split("\n\n")]
    return inp_content


def rotate1(x, y, z): return x, y, z
def rotate2(x, y, z): return x, z, -y
def rotate3(x, y, z): return x, -y, -z
def rotate4(x, y, z): return x, -z, y
def transform1(x, y, z): return x, y, z
def transform2(x, y, z): return -z, y, x
def transform3(x, y, z): return -z, y, -x
def transform4(x, y, z): return -z, -y, x
def transform5(x, y, z): return -z, -y, -x
def transform6(x, y, z): return -z, -y, -x


def transform(field: set[tuple[int, int, int]], func) -> set[tuple[int, int, int]]:
    f: set[tuple[int, int, int]] = set()
    for x, y, z in field:
        f.add(func(x, y, z))
    return field


def adjust(field1: set[tuple[int, int, int]], field2: set[tuple[int, int, int]], size=12) -> Optional[set[tuple[int, int, int]]]:
    for x1, y1, z1 in field1:
        for x2, y2, z2 in field2:
            xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
            res = set()
            for x3, y3, z3 in field2:
                res.add((x3 - xd, y3 - yd, z3 - zd))
            if len(field1.intersection(res)) >= size:
                return res
    return None


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = parse_input(input_str)
    res = inp[0]
    inp.remove(res)
    while inp:
        print(len(inp), len(res))
        works = False
        for j, f2 in enumerate(inp):
            for transform_ in [transform1, transform2, transform3, transform4, transform5, transform6]:
                f2_ = transform(f2, transform_)
                for rotate in [rotate1, rotate2, rotate3, rotate4]:
                    f2__ = transform(f2_, rotate)
                    f2__ = adjust(res, f2__)
                    if f2__ is not None:
                        print(transform_.__name__, rotate.__name__)
                        res = res.union(f2__)
                        inp.remove(f2)
                        works = True
                        break
                if works:
                    break
            if works:
                break
    correct = parse_input("""\n-892,524,684
-876,649,763
-838,591,734
-789,900,-551
-739,-1745,668
-706,-3180,-659
-697,-3072,-689
-689,845,-530
-687,-1600,576
-661,-816,-575
-654,-3158,-753
-635,-1737,486
-631,-672,1502
-624,-1620,1868
-620,-3212,371
-618,-824,-621
-612,-1695,1788
-601,-1648,-643
-584,868,-557
-537,-823,-458
-532,-1715,1894
-518,-1681,-600
-499,-1607,-770
-485,-357,347
-470,-3283,303
-456,-621,1527
-447,-329,318
-430,-3130,366
-413,-627,1469
-345,-311,381
-36,-1284,1171
-27,-1108,-65
7,-33,-71
12,-2351,-103
26,-1119,1091
346,-2985,342
366,-3059,397
377,-2827,367
390,-675,-793
396,-1931,-563
404,-588,-901
408,-1815,803
423,-701,434
432,-2009,850
443,580,662
455,729,728
456,-540,1869
459,-707,401
465,-695,1988
474,580,667
496,-1584,1900
497,-1838,-617
527,-524,1933
528,-643,409
534,-1912,768
544,-627,-890
553,345,-567
564,392,-477
568,-2007,-577
605,-1665,1952
612,-1593,1893
630,319,-379
686,-3108,-505
776,-3184,-501
846,-3110,-434
1135,-1161,1235
1243,-1093,1063
1660,-552,429
1693,-557,386
1735,-437,1738
1749,-1800,1813
1772,-405,1572
1776,-675,371
1779,-442,1789
1780,-1548,337
1786,-1538,337
1847,-1591,415
1889,-1729,1762
1994,-1805,1792""")[0]

    missing = correct - res.intersection(correct)
    return len(res)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


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
