def nr1(instructions: list[str]) -> int:
    i = 0
    acc = 0
    performed_instructions = []
    while i not in performed_instructions:
        ins, val = instructions[i].split()
        performed_instructions.append(i)
        val = int(val)
        if ins == "acc":
            acc += val
        elif ins == "jmp":
            i += val - 1
        i += 1
    return acc


def nr2(i: int, instructions: list[str], used: list[int], acc: int, inst: bool) -> tuple[int, bool]:
    if i >= len(instructions):
        return acc, True
    if i in used:
        return acc, False
    ins, val = instructions[i].split()
    used.append(i)
    val = int(val)
    if ins == "acc":
        return nr2(i + 1, instructions, used, acc + val, inst)
    elif ins == "jmp":
        acc_, worked = nr2(i + val, instructions, used, acc, inst)
        if worked or inst:
            return acc_, worked
        return nr2(i + 1, instructions, used, acc, True)
    else:
        acc_, worked = nr2(i + 1, instructions, used, acc, inst)
        if worked or inst:
            return acc_, worked
        return nr2(i + val, instructions, used, acc, True)


def main():
    with open("inputs/day_08.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(s))
    print(nr2(0, s, [], 0, False))


if __name__ == "__main__":
    main()
