def seat(seat_str: str) -> int:
    return int(seat_str[:7].replace("B", "1").replace("F", "0"), 2) * 8 + int(seat_str[7:].replace("R", "1").replace("L", "0"), 2)


def seats(seats_str: list[str]) -> list[int]:
    return [seat(s) for s in seats_str]


def nr1(seats_) -> int:
    return max(seats_)


def nr2(seats_, m_s) -> int:
    return (m_s * (m_s + 1)) // 2 - sum(seats_) - min(seats_) * (min(seats_) - 1) // 2


def main():
    with open("inputs/day_05.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    seats_ = seats(s)
    m_s = nr1(seats_)
    print(m_s)
    print(nr2(seats_, m_s))


if __name__ == "__main__":
    main()
