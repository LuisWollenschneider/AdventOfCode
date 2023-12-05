from utils import aoc_comm, create_test_file
import os
from typing import Optional

# --- update day/ year for each challenge
settings = {
    'day': 5,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools
import re


class ConversionRange:
    def __init__(self, dest_val, source_val, r):
        self.source_val = source_val
        self.dest_val = dest_val
        self.r = r

    def __contains__(self, item):
        return self.source_val <= item < self.source_val + self.r

    def get_val(self, item):
        return self.dest_val + (item - self.source_val)

    def get_end(self):
        return self.source_val + self.r - 1

    def remaining_range(self, item):
        return self.r - (item - self.source_val)

    def __repr__(self):
        return f"{self.source_val} - {self.source_val + self.r - 1} -> {self.dest_val} - {self.dest_val + self.r - 1}"


def get_lowest_destination(seeds, inp):
    conversions = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    conversions_dict = {}

    for i, c in enumerate(conversions, start=1):
        conversions_dict[c] = {
            ConversionRange(*map(int, line.split())) for line in inp[i].split('\n')[1:]
        }

    start = seeds
    end = []

    for c in conversions:
        while start:
            el, r = start.pop()

            for cr in conversions_dict[c]:
                if el not in cr:
                    continue
                s = cr.get_val(el)
                r_ = min(r, cr.remaining_range(el))
                end.append((s, r_))
                if r_ < r:
                    start.append((el + r_, r - r_))
                break
            else:
                next_min = [cr.source_val for cr in conversions_dict[c] if cr.source_val > el]
                if next_min:
                    next_min = min(next_min)
                    end.append((el, min(next_min - el, r)))
                    if el + r - next_min > 0:
                        start.append((next_min, el + r - next_min))
                    continue
                end.append((el, r))
        start = end
        end = []

    return min(start, key=lambda x: x[0])[0]


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = input_str.split('\n\n')
    seeds = [(el, 1) for el in map(int, inp[0].split(":")[1].strip().split())]

    return get_lowest_destination(seeds, inp)


@aoc_comm(settings, level=2, debug=True)
def solve_l2(input_str) -> Optional[int]:
    inp = input_str.split('\n\n')
    seeds = list(map(int, inp[0].split(":")[1].strip().split()))

    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

    return get_lowest_destination(seeds, inp)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
