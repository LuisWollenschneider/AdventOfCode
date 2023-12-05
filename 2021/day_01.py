def comp_to_k_before(n: list[int], k: int) -> int:
    c = 0
    for i, x in enumerate(n[k:]):
        if x > n[i]:
            c += 1
    return c


def nr1(n: list[int]) -> int:
    return comp_to_k_before(n, 1)


def nr2(n: list[int]) -> int:
    return comp_to_k_before(n, 3)


def main():
    with open("inputs/day_01.txt", "r") as f:
        s = [int(el.replace("\n", "")) for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
