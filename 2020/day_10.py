from functools import lru_cache


def nr1(n) -> int:
    jolt = 0
    count1, count3 = 0, 1
    while jolt < max(n):
        if jolt + 1 in n:
            count1 += 1
            jolt += 1
        elif jolt + 2 in n:
            jolt += 2
        elif jolt + 3 in n:
            jolt += 3
            count3 += 1
        else:
            return -1
    return count1 * count3


@lru_cache(maxsize=256)
def nr2(i):
    if i == len(n) - 1:
        return 1
    return sum(
        [
            nr2(j)
            for j in range(i + 1, min(i + 4, len(n)))
            if n[j] - n[i] <= 3
        ]
    )


def main():
    with open("inputs/day_10.txt", "r") as f:
        s = [int(el.replace("\n", "")) for el in f.readlines()]
    print(nr1(s))
    print(nr2(0))


if __name__ == "__main__":
    with open("inputs/day_10.txt", "r") as f:
        s = [int(el.replace("\n", "")) for el in f.readlines()]
    print(nr1(s))
    n = sorted(s + [0, max(s) + 3])
    main()
