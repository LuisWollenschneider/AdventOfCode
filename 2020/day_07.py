def has_gold(b, bags) -> bool:
    if b not in bags:
        return False
    for inner_bag in bags[b]:
        if "shiny gold" in inner_bag:
            return True
    return any([has_gold(inner_bag[2:], bags) for inner_bag in bags[b]])


def nr1(bags) -> int:
    return [has_gold(b, bags) for b in bags].count(True)


def nr2(b, bags) -> int:
    if b not in bags:
        return 0
    return sum([int(inner_bag[0]) + nr2(inner_bag[2:], bags) for inner_bag in bags[b]])


def main():
    bags = {}
    with open("inputs/day_07.txt", "r") as f:
        for el in f.readlines():
            c, cont = el.split(" bags contain ")
            bags[c] = [e.replace("bags", "").replace("bag", "").replace('.', '').replace('no', '0').strip() for e in cont.split(",")]

    # print(bags)
    print(nr1(bags))
    print(nr2("shiny gold", bags))


if __name__ == "__main__":
    main()
