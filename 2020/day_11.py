def get_seats_around(seats, x, y):
    adjacent_seats = ""
    idx = [-1, 0, 1]
    for i in idx:
        if 0 <= x + i < len(seats):
            for j in idx:
                if 0 <= y + j < len(seats[x]):
                    if not (i == 0 and j == 0):
                        adjacent_seats += seats[x+i][y+j]
    return adjacent_seats


def get_seats_in_range(seats, x, y):
    adjacent_seats = ""
    idx = [-1, 0, 1]
    for i in idx:
        if 0 <= x + i < len(seats):
            for j in idx:
                if 0 <= y + j < len(seats[x]):
                    if not (i == 0 and j == 0):
                        i_, j_ = 0, 0
                        c = False
                        while seats[x+i+i_][y+j+j_] == ".":
                            i_ += i
                            j_ += j
                            if not (0 <= x + i + i_ < len(seats)):
                                c = True
                                break
                            if not (0 <= y + j + j_ < len(seats[x])):
                                c = True
                                break
                        if c:
                            continue
                        adjacent_seats += seats[x+i+i_][y+j+j_]
    return adjacent_seats


def nr1(seats) -> int:
    new_seats = []
    for x in range(len(seats)):
        new_seats.append("")
        for y, s in enumerate(seats[x]):
            if s == ".":
                new_seats[-1] += "."
            elif s == "L":
                new_seats[-1] += "#" if "#" not in get_seats_around(seats, x, y) else "L"
            else:
                new_seats[-1] += "L" if get_seats_around(seats, x, y).count("#") >= 4 else "#"
    if new_seats == seats:
        return sum([s.count("#") for s in new_seats])
    return nr1(new_seats)


def nr2(seats) -> int:
    new_seats = []
    for x in range(len(seats)):
        new_seats.append("")
        for y, s in enumerate(seats[x]):
            if s == ".":
                new_seats[-1] += "."
            elif s == "L":
                new_seats[-1] += "#" if "#" not in get_seats_in_range(seats, x, y) else "L"
            else:
                new_seats[-1] += "L" if get_seats_in_range(seats, x, y).count("#") >= 5 else "#"
    if new_seats == seats:
        return sum([s.count("#") for s in new_seats])
    return nr2(new_seats)


def main():
    with open("inputs/day_11.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    # print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
