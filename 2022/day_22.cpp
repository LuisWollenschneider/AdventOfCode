//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "22"
#define YEAR "2022"
#define RETURN_TYPE int

struct Tuple {
    std::vector<std::string> map;
    std::string path;
};

#define TYPE Tuple

TYPE parse_input(const std::string &filepath) {
    // check if path exists
    TYPE input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    input.map.push_back(" ");
    int l = 0;
    while (std::getline(file, line)) {
        if (line.empty()) {
            break;
        }
        input.map.push_back(line);
        l = std::max(l, (int) line.length());
    }
    l++;
    input.map.push_back(" ");
    for (int i = 0; i < input.map.size(); i++) {
        input.map[i] = " " + input.map[i] + std::string(l - input.map[i].length(), ' ');
    }

    while (std::getline(file, line)) {
        input.path = line;
    }
    file.close();
    return input;
}

bool rotate(int* dx, int* dy, char c) {
    switch (c) {
        case 'L': {
            if (*dx != 0) {
                *dy = - *dx;
                *dx = 0;
            } else {
                *dx = *dy;
                *dy = 0;
            }
            break;
        }
        case 'R': {
            if (*dx != 0) {
                *dy = *dx;
                *dx = 0;
            } else {
                *dx = -*dy;
                *dy = 0;
            }
            break;
        }
        default: {
            return false;
        }
    }
    return true;
}

int dir(int dx, int dy) {
    if (dx == 1) {
        return 0;
    } else if (dy == 1) {
        return 1;
    } else if (dx == -1) {
        return 2;
    } else if (dy == -1) {
        return 3;
    }
    return -1;
}


RETURN_TYPE part1(TYPE &inp) {
    int x = 0;
    int y = 1;
    while (inp.map[y][x] == ' ') {
        x++;
    }

    int dx = 1;
    int dy = 0;
    std::map<int, std::map<int, char> > arrow;
    arrow[-1] = std::map<int, char>();
    arrow[0] = std::map<int, char>();
    arrow[1] = std::map<int, char>();
    arrow[0][-1] = '<';
    arrow[0][1] = '>';
    arrow[-1][0] = '^';
    arrow[1][0] = 'v';

    while (!inp.path.empty()) {
        if (rotate(&dx, &dy, inp.path[0])) {
            inp.path.erase(0, 1);
            continue;
        }
        int steps = std::stoi(inp.path);
        inp.path.erase(0, std::to_string(steps).length());
        for (int i = 0; i < steps; i++) {
            int nx = x + dx;
            int ny = y + dy;
            if (dy != 0 && inp.map[ny][nx] == ' ') {
                ny -= dy;
                while (inp.map[ny][nx] != ' ') {
                    ny -= dy;
                }
                ny += dy;
            } else if (dx != 0 && inp.map[ny][nx] == ' ') {
                nx -= dx;
                while (inp.map[ny][nx] != ' ') {
                    nx -= dx;
                }
                nx += dx;
            }
            if (inp.map[ny][nx] == '#') {
                break;
            }
            inp.map[y][x] = arrow[dy][dx];
            x = nx;
            y = ny;
        }

    }

    /*
    inp.map[y][x] = 'X';
    for (int i = 0; i < inp.map.size(); i++) {
        std::cout << inp.map[i] << std::endl;
    }
    std::cout << std::endl;
    */

    return 1000 * y + 4 * x + dir(dx, dy);
}

int edges(int x, int y, const std::vector<std::string>* map) {
    int res = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) {
                continue;
            }
            if ((*map)[y + i][x + j] == ' ') {
                res++;
            }
        }
    }
    return res;
}

RETURN_TYPE part2(TYPE &inp) {
    int x = 0;
    int y = 1;
    while (inp.map[y][x] == ' ') {
        x++;
    }

    int dx = 1;
    int dy = 0;
    std::map<int, std::map<int, char> > arrow;
    arrow[-1] = std::map<int, char>();
    arrow[0] = std::map<int, char>();
    arrow[1] = std::map<int, char>();
    arrow[0][-1] = '<';
    arrow[0][1] = '>';
    arrow[-1][0] = '^';
    arrow[1][0] = 'v';

    while (!inp.path.empty()) {
        if (rotate(&dx, &dy, inp.path[0])) {
            inp.path.erase(0, 1);
            continue;
        }
        int steps = std::stoi(inp.path);
        inp.path.erase(0, std::to_string(steps).length());
        for (int i = 0; i < steps; i++) {
            int nx = x + dx;
            int ny = y + dy;
            int ndx = dx;
            int ndy = dy;
            if (inp.map[ny][nx] == ' ') {
                ny -= ndy;
                nx -= ndx;
                // inp.map[ny][nx] = 'A';
                int dist = 0;
                int d = 1;
                rotate(&ndx, &ndy, 'R');
                while (dist != 0 || (nx == x && ny == y)) {
                    ny += ndy;
                    nx += ndx;
                    dist += d;
                    if (dist == 0) {
                        break;
                    }
                    if (nx == 150 && ny == 1 && ndx == 1) {
                        d = -d;
                        nx = 50;
                        ny = 200;
                        ndx = -1;
                        continue;
                    }
                    if (nx == 100 && ny == 150 && ndy == 1) {
                        d = -d;
                        nx = 150;
                        ny = 1;
                        continue;
                    }
                    if (nx == 50 && ny == 200 && ndy == 1) {
                        d = -d;
                        nx = 100;
                        ny = 150;
                        ndy = 0;
                        ndx = -1;
                        continue;
                    }
                    int ed = edges(nx, ny, &inp.map);
                    if (ed == 1) {
                        rotate(&ndx, &ndy, 'L');
                        d = -d;
                    } else if (ed == 5) {
                        rotate(&ndx, &ndy, 'R');
                        dist += d;
                    }
                }
                rotate(&ndx, &ndy, 'R');
                // inp.map[ny][nx] = 'B';
            }
            if (inp.map[ny][nx] == '#') {
                break;
            }
            inp.map[y][x] = arrow[dy][dx];
            x = nx;
            y = ny;
            dx = ndx;
            dy = ndy;
        }

    }


    inp.map[y][x] = 'X';
    for (int i = 0; i < inp.map.size(); i++) {
        std::cout << inp.map[i] << std::endl;
    }
    std::cout << std::endl;

    std::cout << "x: " << x << " y: " << y << " dir: " << dir(dx, dy) << std::endl;
    return 1000 * y + 4 * x + dir(dx, dy);;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    RETURN_TYPE expected_result_part1 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_1.txt");

    RETURN_TYPE res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::set<RETURN_TYPE> tried;
    tried.insert(113210);
    tried_before(res, tried);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    std::cout << std::endl;
    RETURN_TYPE expected_result_part2 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<RETURN_TYPE> tried2;
    tried2.insert(75305);
    tried2.insert(75306);
    tried2.insert(127368);
    tried_before(res, tried2);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
