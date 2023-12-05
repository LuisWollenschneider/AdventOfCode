def nr1(n) -> int:
    posx, posy = 0, 0
    for x1, x2 in n:
        x2 = int(x2)
        if x1 == "forward":
            posx += x2
        if x1 == "up":
            posy -= x2
        if x1 == "down":
            posy += x2
    return posx * posy


def nr2(n) -> int:
    posx, posy = 0, 0
    aim = 0
    for x1, x2 in n:
        x2 = int(x2)
        if x1 == "forward":
            posx += x2
            posy += aim * x2
        if x1 == "up":
            aim -= x2
        if x1 == "down":
            aim += x2
    return posx * posy


def main():
    with open("inputs/day_02.txt", "r") as f:
        s = [el.replace("\n", "").split() for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
