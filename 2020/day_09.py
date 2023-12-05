from day_01 import two_sum


def nr1(n) -> int:
    stack = n[:25]
    for x in n[25:]:
        if two_sum(stack, x) == (0, 0):
            return x
        stack.append(x)
        stack.pop(0)
    return 0


def nr2(n, k) -> int:
    stack = n[:2]
    for x in n[2:]:
        stack.append(x)
        while sum(stack) > k:
            stack.pop(0)
        if sum(stack) == k and len(stack) >= 2:
            return min(stack) + max(stack)
    return 0


def main():
    with open("inputs/day_09.txt", "r") as f:
        s = [int(el.replace("\n", "")) for el in f.readlines()]
    x = nr1(s)
    print(x)
    print(nr2(s, x))


if __name__ == "__main__":
    main()
