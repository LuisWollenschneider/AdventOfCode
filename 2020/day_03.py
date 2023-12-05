def encounter(s: list[str], x=0, y=0, down=1, right=1) -> int:
    if y >= len(s):
        return 0
    x = x % len(s[y])
    return (1 if s[y][x] == "#" else 0) + encounter(s, x + right, y + down, down, right)


def nr1(s: list[str]) -> int:
    return encounter(s, down=1, right=3)


def nr2(s: list[str]) -> int:
    x = [
        encounter(s, down=1, right=1),
        encounter(s, down=1, right=3),
        encounter(s, down=1, right=5),
        encounter(s, down=1, right=7),
        encounter(s, down=2, right=1),
    ]
    c = 1
    for i in x:
        c *= i
    return c


def main():
    with open("inputs/day_03.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
