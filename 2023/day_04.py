from utils import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 4,
    'year': 2023,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import *
import functools
import itertools


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    inp = input_str.split('\n')

    s = 0
    for card in inp:
        card, numbers = card.split(":")
        winning_numbers, selected_numbers = numbers.split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        selected_numbers = set(map(int, selected_numbers.split()))
        correct = winning_numbers & selected_numbers
        if len(correct) == 0:
            continue
        s += 2 ** (len(correct) - 1)
    return int(s)


@aoc_comm(settings, level=2)
def solve_l2(input_str) -> Optional[int]:
    inp = input_str.split('\n')
    dups = {i + 1: 1 for i in range(len(inp))}

    s = 0
    for card in inp:
        card, numbers = card.split(":")
        card_num = int(card.split()[1])
        winning_numbers, selected_numbers = numbers.split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        selected_numbers = set(map(int, selected_numbers.split()))
        correct = winning_numbers & selected_numbers

        s += dups[card_num]
        for i in range(1, len(correct) + 1):
            dups[card_num + i] += dups[card_num]
    return int(s)


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
