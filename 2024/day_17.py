from utils_py import aoc_comm, create_test_file
import os
from typing import Optional
import re

# --- update day/ year for each challenge
settings = {
    'day': 17,
    'year': 2024,
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

    registers, program = inp_content.split("\n\n")
    registers = list(map(lambda x: int(x.split(": ")[1]), registers.split("\n")))
    program = list(map(lambda x: int(x), program.split(": ")[1].split(",")))

    return registers, program


def execute(registers, program):
    program_counter = 0
    out = []

    while program_counter < len(program):
        opcode = program[program_counter]
        operand = program[program_counter + 1]

        if 4 <= operand < 7:
            combo_operand = registers[operand - 4]
        else:
            combo_operand = operand

        if opcode == 0:  # adv
            registers[0] >>= combo_operand
        elif opcode == 1:  # bxl
            registers[1] ^= operand
        elif opcode == 2:  # bst
            registers[1] = combo_operand & 0x7
        elif opcode == 3:  # jnz
            if registers[0] != 0:
                program_counter = operand
                continue
        elif opcode == 4:  # bxc
            registers[1] ^= registers[2]
        elif opcode == 5:  # out
            out.append(combo_operand & 0x7)
        elif opcode == 6:  # bdv
            registers[1] = registers[0] >> combo_operand
        elif opcode == 7:  # cdv
            registers[2] = registers[0] >> combo_operand

        # print(f"{opcode},{operand}", registers)
        program_counter += 2

    return out


@aoc_comm(settings, level=1)
def solve_l1(input_str) -> Optional[str]:  # input data will be passed to this as string
    registers, program = parse_input(input_str)

    return ",".join(map(str, execute(registers, program)))


@aoc_comm(settings, level=2)
def solve_l2(input_str, output=False) -> Optional[int]:
    registers, program = parse_input(input_str)

    if output:
        print()

    found = 0
    rev = program[::-1]

    registers[0] = 0
    while True:
        out = execute(registers.copy(), program)[::-1]

        if all(o == r for o, r in zip(out, rev)):
            if out == rev:
                return registers[0]

            new_found = len(out)
            if new_found > found:
                if output:
                    # GREEN
                    print("\033[91m", end="")
                    print(",".join(map(str, program[:len(program) - len(out)])), end="")
                    # RED
                    print("\033[0m,\033[92m", end="")
                    print(','.join(map(str, out[::-1])), end="")
                    # RESET
                    print(f"\033[0m {registers[0]}")

                registers[0] <<= 3 * (new_found - found)
                found = new_found
                continue

        registers[0] += 1


def main():
    # create_test_file(settings, int(input("Test file for level: ")), input("Test result: ").strip())
    solve_l1()
    solve_l2()


if __name__ == '__main__':
    main()
