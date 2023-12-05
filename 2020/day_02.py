def get_values(line: str) -> tuple[int, int, str, str]:
    r, c, inp = line.split()
    r1, r2 = r.split("-")
    r1, r2 = int(r1), int(r2)
    c = c.replace(":", "")
    return r1, r2, c, inp


def nr1(s) -> int:
    d = {True: 0, False: 0}
    for l in s:
        r1, r2, c, inp = get_values(l)
        d[r1 <= inp.count(c) <= r2] += 1
    return d[True]


def nr2(s) -> int:
    d = {True: 0, False: 0}
    for l in s:
        r1, r2, c, inp = get_values(l)
        d[(inp[r1-1] == c) ^ (inp[r2-1] == c)] += 1
    return d[True]


def main():
    with open("inputs/day_02.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
