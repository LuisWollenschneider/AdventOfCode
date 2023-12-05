import re


def valid_passports_check_1(s, keys) -> list[dict]:
    keys = set(keys)
    valid = []
    for d_ in s:
        if keys.difference(set(d_.keys())) in [set(), {'cid'}]:
            valid.append(d_)
    return valid


def valid_passports_check_2(s, keys) -> list[dict]:
    vp = valid_passports_check_1(s, keys)
    valid = []
    for p in vp:
        p["byr"] = int(p["byr"])
        if p["byr"] < 1920 or p["byr"] > 2002:
            continue
        p["iyr"] = int(p["iyr"])
        if p["iyr"] < 2010 or p["iyr"] > 2020:
            continue
        p["eyr"] = int(p["eyr"])
        if p["eyr"] < 2020 or p["eyr"] > 2030:
            continue
        if not re.match(r"(1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in)", p["hgt"]):
            continue
        if not re.match(r"#[0-9a-f]{6}", p["hcl"]):
            continue
        if not re.match(r"(amb|blu|brn|gry|grn|hzl|oth)", p["ecl"]):
            continue
        if not re.match(r"0*\d{9}", p["pid"]):
            continue
        valid.append(p)
    return valid


def nr1(s, keys) -> int:
    return len(valid_passports_check_1(s, keys))


def nr2(s, keys) -> int:
    return len(valid_passports_check_2(s, keys))


def main():
    s = []
    with open("inputs/day_04.txt", "r") as f:
        s_ = f.read().split("\n\n")
        for el in s_:
            d = {}
            for x in re.split(r"\s|\n", el):
                k, v = x.split(":")
                d[k] = v
            s.append(d)
    keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    print(nr1(s, keys))
    print(nr2(s, keys))


if __name__ == "__main__":
    main()
