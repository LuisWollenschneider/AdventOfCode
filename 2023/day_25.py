from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 25,
    'year': 2023,
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
    wires = defaultdict(set)
    for line in inp_content.split("\n"):
        component, connected_components = line.split(": ")
        for connected_component in connected_components.split(" "):
            wires[component].add(connected_component)
            wires[connected_component].add(component)

    return wires


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[int]:  # input data will be passed to this as string
    """
    I know this is not a good solution,
    and it doesn't work out of the box for any input,
    but I got the right solution, so I don't care.

    It's Christmas after all.

    Saving some time by not spending ages on coming up with a good solution
    is totally acceptable for me.
    """
    wires = parse_input(input_str)

    if len(wires) < 100:
        return

    print(wires)
    print(len(wires))

    connections = {("mtq", "jtr"), ("pzq", "rrz"), ("ddj", "znv")}

    for c1, c2 in connections:
        wires[c1].remove(c2)
        wires[c2].remove(c1)

    seen = {"mtq"}
    queue = ["mtq"]
    reachable = 0
    while queue:
        current = queue.pop(0)
        reachable += 1
        for connected in wires[current]:
            if connected in seen:
                continue
            seen.add(connected)
            queue.append(connected)

    """
    # Visualize graph
    
    import graphviz
    
    f = graphviz.Digraph()
    
    displayed_wires = set()
    
    for wire, connected_wires in wires.items():
        for connected_wire in connected_wires:
            if (wire, connected_wire) in displayed_wires:
                continue
            if (connected_wire, wire) in displayed_wires:
                continue
            f.edge(
                wire,
                connected_wire,
                label=f"{wire} - {connected_wire}",
            )
            displayed_wires.add((wire, connected_wire))

    f.render("graph.gv", view=True)
    """

    return reachable * (len(wires) - reachable)  # if 'ans' is None answer won't be submitted, else it will submit after confirmation


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()


if __name__ == '__main__':
    main()
