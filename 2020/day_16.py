def get_rules(rules: list[str]) -> list[tuple[str, int, int, int, int]]:
    r: list[tuple[str, int, int, int, int]] = []
    for rule in rules:
        r_name, r_rest = rule.split(": ")
        r_min_max_1, r_min_max_2 = r_rest.split(" or ")
        r_min_1, r_max_1 = r_min_max_1.split("-")
        r_min_2, r_max_2 = r_min_max_2.split("-")
        r_min_1, r_max_1, r_min_2, r_max_2 = int(r_min_1), int(r_max_1), int(r_min_2), int(r_max_2)
        r.append((r_name, r_min_1, r_max_1, r_min_2, r_max_2))
    return r


def find_valid_tickets(rules: list[tuple[str, int, int, int, int]], tickets: list[list[int]]) -> list[list[int]]:
    valid = []
    c = 0
    for ticket in tickets:
        invalid = False
        for field in ticket:
            if all([not (r[1] <= field <= r[2] or r[3] <= field <= r[4]) for r in rules]):
                invalid = True
                c += field
                break
        if invalid:
            continue
        valid.append(ticket)
    print(c)
    return valid


def find_valid_rules(rules: list[tuple[str, int, int, int, int]], tickets: list[list[int]], i: int) -> list[tuple[str, int, int, int, int]]:
    r = []
    for rule in rules:
        if any([not (rule[1] <= ticket[i] <= rule[2] or rule[3] <= ticket[i] <= rule[4]) for ticket in tickets]):
            continue
        r.append(rule)
    return r


def nr1(sections) -> int:
    rules = sections[0].split("\n")
    my_ticket: list[int] = [int(n) for n in sections[1].split("\n")[1].split(",")]
    tickets: list[list[int]] = []
    for t in sections[2].split("\n")[1:]:
        tickets.append([])
        for n in t.split(","):
            tickets[-1].append(int(n))
    rules = get_rules(rules)
    tickets = find_valid_tickets(rules, tickets)
    d = {}
    tickets.append(my_ticket)
    for i in range(len(my_ticket)):
        d[i] = find_valid_rules(rules, tickets, i)
    d_ = d.copy()
    changed = True
    while changed:
        changed = False
        for j, rs in d_.items():
            if len(rs) == 1:
                for i, rs_ in d_.items():
                    if rs[0] in d[i]:
                        if i != j:
                            d[i].remove(rs[0])
                            changed = True
    c = 1
    for i, rule in d.items():
        if rule[0][0].startswith("departure"):
            c *= my_ticket[i]
    print(c)
    return 0


def nr2() -> int:
    return 0


def main():
    with open("inputs/day_16.txt", "r") as f:
        s = f.read().split("\n\n")
    print(nr1(s))
    print(nr2())


if __name__ == "__main__":
    main()
