//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.h"
#include <cmath>

#define DAY "24"
#define YEAR "2022"
#define RETURN_TYPE int

struct Direction {
    int dx;
    int dy;
};

#define TYPE std::map<long long, std::vector<Direction> >*

long long pair(long long x, long long y) {
    // map coordinates to a unique number in N
    // map N^2 to N using Cantor pairing function
    return (x + y) * (x + y + 1) / 2 + y;
}

TYPE parse_input(const std::string &filepath) {
    // check if path exists
    TYPE input = new std::map<long long, std::vector<Direction> >();
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    Direction up = {
            .dx = 0,
            .dy = -1
    };
    Direction down = {
            .dx = 0,
            .dy = 1
    };
    Direction right = {
            .dx = 1,
            .dy = 0
    };
    Direction left = {
            .dx = -1,
            .dy = 0
    };
    long long y = 0;
    while (std::getline(file, line)) {
        for (long long x = 0; x < line.length(); x++) {
            if (line[x] == '>') {
                (*input)[pair(x, y)].push_back(right);
            } else if (line[x] == '<') {
                (*input)[pair(x, y)].push_back(left);
            } else if (line[x] == '^') {
                (*input)[pair(x, y)].push_back(up);
            } else if (line[x] == 'v') {
                (*input)[pair(x, y)].push_back(down);
            }
        }
        y++;
    }
    file.close();
    return input;
}

long long pi2(long long c) {
    // map N to N^2 using inverse Cantor pairing function
    long long w = floor((sqrt(8 * c + 1) - 1) / 2);
    long long t = (w * w + w) / 2;
    long long y = c - t;
    return w - y;
    // map N to Z
}

long long pi1(long long c) {
    // map N to N^2 using inverse Cantor pairing function
    long long w = floor((sqrt(8 * c + 1) - 1) / 2);
    long long t = (w * w + w) / 2;
    return c - t;
}

void move(TYPE inp, int h, int w) {
    TYPE out = new std::map<long long, std::vector<Direction> >();
    for (auto p : *inp) {
        long long k = p.first;
        long long x = pi2(k);
        long long y = pi1(k);
        for (auto direction : p.second) {
            int x2 = x + direction.dx;
            if (x2 == 0) {
                x2 = w - 1;
            } else if (x2 == w) {
                x2 = 1;
            }
            int y2 = y + direction.dy;
            if (y2 == 0) {
                y2 = h - 1;
            } else if (y2 == h) {
                y2 = 1;
            }
            (*out)[pair(x2, y2)].push_back(direction);
        }
    }
    *inp = *out;
}

void show(TYPE inp, int h, int w, std::set<long long>* pos) {
    for (int x = 0; x <= w; x++) {
        if (x == 1) {
            if (pos->find(pair(x, 0)) != pos->end()) {
                std::cout << COLOR_MAGENTA << 'E' << COLOR_RESET;
            } else {
                std::cout << '.';
            }
        } else {
            std::cout << "#";
        }
    }
    std::cout << std::endl;
    for (int y = 1; y < h; y++) {
        std::cout << "#";
        for (int x = 1; x < w; x++) {
            if (pos->find(pair(x, y)) != pos->end()) {
                std::cout << COLOR_MAGENTA;
            } else {
                std::cout << COLOR_RESET;
            }
            if (inp->find(pair(x, y)) != inp->end()) {
                std::vector<Direction> ds = (*inp)[pair(x, y)];
                if (ds.size() == 1) {
                    if (ds[0].dx == 1) {
                        std::cout << ">";
                    } else if (ds[0].dx == -1) {
                        std::cout << "<";
                    } else if (ds[0].dy == 1) {
                        std::cout << "v";
                    } else if (ds[0].dy == -1) {
                        std::cout << "^";
                    }
                } else {
                    std::cout << ds.size();
                }
            } else {
                std::cout << ".";
            }
        }
        std::cout << COLOR_RESET << '#' << std::endl;
    }
    for (int x = 0; x <= w; x++) {
        if (x == w-1) {
            if (pos->find(pair(x, h)) != pos->end()) {
                std::cout << COLOR_MAGENTA << 'E' << COLOR_RESET;
            } else {
                std::cout << '.';
            }
        } else {
            std::cout << "#";
        }
    }
    std::cout << std::endl;
    std::cout << std::endl;
}

int traverse(TYPE inp, int h, int w, std::set<long long>* pos, int c, int targetx, int targety) {
    // std::cout << "Minute " << c << std::endl;
    // show(inp, h, w, pos);
    move(inp, h, w);
    std::set<long long> new_pos;
    for (auto p : *pos) {
        if (p < 0) {
            continue;
        }
        long long x = pi2(p);
        long long y = pi1(p);
        if (x == targetx && y == targety) {
            return c;
        }
        std::vector<long long> ps;
        if ((x <= 0 || x >= w || y <= 0 || y >= h)) {
            if (x == 1 && y == 0) {
                ps.push_back(pair(x, y));
                ps.push_back(pair(x, y+1));
            } else if (x == w -1 && y == h) {
                ps.push_back(pair(x, y));
                ps.push_back(pair(x, y - 1));
            } else {
                continue;
            }
        } else {
            ps.push_back(p);
            ps.push_back(pair(x + 1, y));
            ps.push_back(pair(x - 1, y));
            ps.push_back(pair(x, y + 1));
            ps.push_back(pair(x, y - 1));
        }
        for (auto p2 : ps) {
            if (inp->find(p2) == inp->end()) {
                new_pos.insert(p2);
            }
        }
    }
    return traverse(inp, h, w, &new_pos, c+1, targetx, targety);
}

RETURN_TYPE part1(TYPE inp) {
    int w = 0;
    int h = 0;
    for (auto p : *inp) {
        long long x = pi2(p.first);
        long long y = pi1(p.first);
        if (x > w) {
            w = (int)x;
        }
        if (y > h) {
            h = (int)y;
        }
    }

    std::set<long long> pos;
    pos.insert(pair(1, 0));
    return traverse(inp, h+1, w+1, &pos, 0, w, h + 1);
}


RETURN_TYPE part2(TYPE inp) {
    RETURN_TYPE res = 0;

    int w = 0;
    int h = 0;
    for (auto p : *inp) {
        long long x = pi2(p.first);
        long long y = pi1(p.first);
        if (x > w) {
            w = (int)x;
        }
        if (y > h) {
            h = (int)y;
        }
    }

    std::set<long long> pos;
    pos.insert(pair(1, 0));
    res += traverse(inp, h+1, w+1, &pos, 0, w, h + 1);
    pos.clear();
    pos.insert(pair(w, h + 1));
    res += traverse(inp, h+1, w+1, &pos, 1, 1, 0);
    pos.clear();
    pos.insert(pair(1, 0));
    res += traverse(inp, h+1, w+1, &pos, 1, w, h + 1);
    return res;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    auto expected_result_part1 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_1.txt");

    RETURN_TYPE res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::set<RETURN_TYPE> tried;
    tried_before(res, tried);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    std::cout << std::endl;
    auto expected_result_part2 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<RETURN_TYPE> tried2;
    tried_before(res, tried2);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
