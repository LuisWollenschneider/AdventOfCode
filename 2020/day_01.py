def two_sum(ns: list[int], k: int) -> tuple[int, int]:
    d = {}
    for x in ns:
        if x in d:
            return x, k-x
        d[k-x] = x
    return 0, 0


def three_sum(ns: list[int], k: int) -> tuple[int, int, int]:
    for i, x in enumerate(ns[:-2]):
        res = two_sum(ns[i+1:], k-x)
        if res != (0, 0):
            return x, res[0], res[1]
    return 0, 0, 0


def nr1(n: list[int]) -> int:
    c = 1
    for x in two_sum(n, 2020):
        c *= x
    return c


def nr2(n: list[int]) -> int:
    c = 1
    for x in three_sum(n, 2020):
        c *= x
    return c


def main():
    with open("inputs/day_01.txt", "r") as f:
        s = [int(el.replace("\n", "")) for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
