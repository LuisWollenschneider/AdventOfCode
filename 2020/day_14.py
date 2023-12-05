def nr1(n) -> int:
    mask = ""
    d = {}
    for ins in n:
        instruction, val = ins.split(" = ")
        if instruction.startswith("mask"):
            mask = val
        if instruction.startswith("mem"):
            add = int(instruction[4:-1])
            val = bin(int(val))
            val = ("0" * (37 - len(val)) + val).replace("b", "")
            v = ""
            for m, v_ in zip(mask, val):
                v += v_ if m == "X" else m
            d[add] = int(v, 2)
    return sum(d.values())


def apply_mask(address: str, rep) -> list[int]:
    if "X" not in address:
        return [int(address, 2)]
    address = address.replace("X", rep, 1)
    return apply_mask(address, "1") + apply_mask(address, "0")


def nr2(n) -> int:
    mask = ""
    d = {}
    for ins in n:
        instruction, val = ins.split(" = ")
        if instruction.startswith("mask"):
            mask = val
        if instruction.startswith("mem"):
            add = bin(int(instruction[4:-1]))
            val = int(val)
            add = ("0" * (37 - len(add)) + add).replace("b", "")
            add_ = ""
            for m, a in zip(mask, add):
                add_ += a if m == "0" else m
            for a in apply_mask(add_, "0") + apply_mask(add_, "1"):
                d[a] = val
    return sum(d.values())


def main():
    with open("inputs/day_14.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
