from string import ascii_lowercase


def nr1(s) -> int:
    c = 0
    for w in s:
        for l in ascii_lowercase:
            if l in w:
                c += 1
    return c


def nr2(s) -> int:
    c = 0
    for g in s:
        for l in ascii_lowercase:
            if all([l in w for w in g.split("\n")]):
                c += 1
    return c


def main():
    with open("inputs/day_06.txt", "r") as f:
        s = [el for el in f.read().split("\n\n")]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
