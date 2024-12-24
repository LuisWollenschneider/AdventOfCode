from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 24,
    'year': 2024,
    'cookie-path': os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the solutions
from collections import Counter, defaultdict
from math import log10
import functools
import itertools


def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    wires, gates = inp_content.split("\n\n")
    ws = {}
    for w in wires.split("\n"):
        wn, wv = w.split(": ")
        ws[wn] = int(wv)

    gs = {}
    for g in gates.split("\n"):
        w1, op, w2, _, ow = g.split()
        gs[ow] = (w1, op, w2)

    return ws, gs


def eval_wire(wire, gates, wires):
    if wire in wires:
        return wires[wire]

    w1, op, w2 = gates[wire]
    w1v = eval_wire(w1, gates, wires)
    w2v = eval_wire(w2, gates, wires)
    if op == "AND":
        wires[wire] = w1v & w2v
    elif op == "OR":
        wires[wire] = w1v | w2v
    elif op == "XOR":
        wires[wire] = w1v ^ w2v
    return wires[wire]


def compute(wires, gates, expected=None):
    end_wires = sorted([ow for ow in gates.keys() if ow.startswith("z")])

    s = 0
    for i, ew in enumerate(end_wires):
        wires[ew] = eval_wire(ew, gates, wires)
        s += wires[ew] << i
        if expected:
            if wires[ew] << i != expected & (1 << i):
                return None

    return s


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    wires, gates = parse_input(input_str)

    return compute(wires, gates)


@aoc_comm(settings, level=2, test_case=False)
def solve_l2(input_str) -> Optional[str]:
    wires, gates = parse_input(input_str)

    x = sum(wv << i for i, wv in enumerate([wv for wn, wv in sorted(wires.items()) if wn.startswith("x")]))
    y = sum(wv << i for i, wv in enumerate([wv for wn, wv in sorted(wires.items()) if wn.startswith("y")]))

    pairs_to_swap = 4

    max_z = max(ow for ow in gates.keys() if ow.startswith("z"))

    broken = set()
    # https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Full-adder_logic_diagram.svg/2560px-Full-adder_logic_diagram.svg.png
    for g, (w1, op, w2) in gates.items():
        if op == "XOR" and not g.startswith("z"):
            if not w1.startswith("x") and not w1.startswith("y"):
                if g in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(g)
                print(f"XOR {g} must come from x or y, not {w1}")
            if not w2.startswith("x") and not w2.startswith("y"):
                if g in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(g)
                print(f"XOR {g} must come from x or y, not {w2}")

        if g.startswith("z") and g != max_z:
            if op != "XOR":
                if g in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(g)
                print(f"{g} must come from XOR, not {op}")

        if op == "AND":
            if {w1, w2} == {"x00", "y00"}:
                continue  # skip the first AND gate as it goes immediately in the carry
            if len([g_ for g_, v in gates.items() if g in v]) != 1:
                if g in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(g)
                print(f"AND {g} must have only one output")

        if op == "OR":
            if gates[w1][1] != "AND":
                if w1 in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(w1)
                print("OR inputs are not AND", w1)
            if gates[w2][1] != "AND":
                if w2 in broken:
                    print("[DUPLICATE]", end=" ")
                broken.add(w2)
                print("OR inputs are not AND", w2)

    if len(broken) != pairs_to_swap * 2:
        print("Wrong number of broken gates")
        return None

    # just to make sure swapping the broken gates, will actually produce the expected result
    for p in itertools.permutations(broken, pairs_to_swap * 2):
        for i in range(0, pairs_to_swap * 2, 2):
            gates[p[i]], gates[p[i + 1]] = gates[p[i + 1]], gates[p[i]]

        try:
            r = compute(wires.copy(), gates, x + y)
            if r is not None:
                return ",".join(sorted(p))
        except:
            pass

        for i in range(0, pairs_to_swap * 2, 2):
            gates[p[i]], gates[p[i + 1]] = gates[p[i + 1]], gates[p[i]]

    return None


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
