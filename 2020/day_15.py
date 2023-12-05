def number_spokern(numbers: list[int], n):
    d = {}
    for i, x in enumerate(numbers[:-1]):
        d[x] = i
    last_number = numbers[-1]
    for i in range(len(numbers), n):
        if last_number not in d:
            new_number = 0
        else:
            new_number = i - d[last_number] - 1
        d[last_number] = i-1
        last_number = new_number
    return last_number


def nr1(numbers: list[int]) -> int:
    return number_spokern(numbers, 2020)


def nr2(numbers: list[int]) -> int:
    return number_spokern(numbers, 30000000)


def main():
    with open("inputs/day_15.txt", "r") as f:
        s = [int(n) for n in f.read().split(",")]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
