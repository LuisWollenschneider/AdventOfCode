def nr1(time, buses) -> int:
    earliest_bus = -1
    diff = 1_000_000_000
    for bus in buses:
        if bus == "x":
            continue
        bus = int(bus)
        next_bus = bus - time % bus
        if next_bus < diff:
            diff = next_bus
            earliest_bus = bus
    return earliest_bus * diff


def nr2(buses) -> int:
    buses = [int(b) for b in buses if b != "x"]
    time_min, time_step = 0, buses[0]
    length = 1
    while True:
        working = True
        offset = -1
        for i, b in enumerate(buses):
            diff = b - time_min % b
            if diff == b:
                diff = 0
            if not (offset < diff <= time_step - len(buses) + i):
                working = False
                if i > length:
                    time_step *= buses[i-1]
                break
            offset = diff
        if working:
            break
        time_min += time_step
    return time_min


def main():
    with open("inputs/day_13.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(int(s[0]), s[1].split(",")))
    # print(nr2(s[1].split(",")))

    # https://0xdf.gitlab.io/adventofcode2020/13
    buses = [int(b) for b in s[1].split(",") if b != "x"]
    from functools import reduce

    def chinese_remainder(n, a):
        sum = 0
        prod = reduce(lambda a, b: a * b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * mul_inv(p, n_i) * p
        return sum % prod

    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1

    offsets = [int(b) - i for i, b in enumerate(s[1].split(",")) if b != 'x']
    print(f'Part 2: {chinese_remainder(buses, offsets)}')


if __name__ == "__main__":
    main()
