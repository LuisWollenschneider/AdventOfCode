def nr1(n) -> int:
    x, y = 0, 0
    facing = (0, 1)
    for i in n:
        ins = i[0]
        val = int(i[1:])
        if ins == "N":
            x += val
        elif ins == "S":
            x -= val
        elif ins == "E":
            y += val
        elif ins == "W":
            y -= val
        elif val == 180:
            facing = (-facing[0], -facing[1])
        elif (val == 90 and ins == "L") or (val == 270 and ins == "R"):
            facing = (facing[1], -facing[0])
        elif (val == 90 and ins == "R") or (val == 270 and ins == "L"):
            facing = (-facing[1], facing[0])
        elif ins == "F":
            x += facing[0] * val
            y += facing[1] * val
    return abs(x) + abs(y)


def nr2(n) -> int:
    x, y = 0, 0
    way_x, way_y = 1, 10
    for i in n:
        ins = i[0]
        val = int(i[1:])
        if ins == "N":
            way_x += val
        elif ins == "S":
            way_x -= val
        elif ins == "E":
            way_y += val
        elif ins == "W":
            way_y -= val
        elif val == 180:
            way_x, way_y = -way_x, -way_y
        elif (val == 90 and ins == "L") or (val == 270 and ins == "R"):
            way_x, way_y = way_y, -way_x
        elif (val == 90 and ins == "R") or (val == 270 and ins == "L"):
            way_x, way_y = -way_y, way_x
        elif ins == "F":
            x += way_x * val
            y += way_y * val
    return abs(x) + abs(y)


def main():
    with open("inputs/day_12.txt", "r") as f:
        s = [el.replace("\n", "") for el in f.readlines()]
    print(nr1(s))
    print(nr2(s))


if __name__ == "__main__":
    main()
