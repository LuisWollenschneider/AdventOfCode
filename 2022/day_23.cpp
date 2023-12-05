//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.h"
#include <cmath>

#define DAY "23"
#define YEAR "2022"
#define RETURN_TYPE int

struct Coordinates {
    int x;
    int y;
};

#define TYPE std::vector<Coordinates>

TYPE parse_input(const std::string &filepath) {
    // check if path exists
    TYPE input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    int y = 0;
    while (std::getline(file, line)) {
        for (int x = 0; x < line.length(); x++) {
            if (line[x] == '#') {
                Coordinates c = {
                    .x = x,
                    .y = y
                };
                input.push_back(c);
            }
        }
        y++;
    }
    file.close();
    return input;
}

int pair(Coordinates c) {
    // map coordinates to a unique number in N
    // map Z to N / positive number -> even, negative number -> odd
    int i = c.x >= 0 ? c.x * 2 : -c.x * 2 - 1;
    int j = c.y >= 0 ? c.y * 2 : -c.y * 2 - 1;
    // map N^2 to N using Cantor pairing function
    return 0.5 * (i + j) * (i + j + 1) + j;
}

int pi2(int c) {
    // map N to N^2 using inverse Cantor pairing function
    int w = floor((sqrt(8 * c + 1) - 1) / 2);
    int t = (w * w + w) / 2;
    int y = c - t;
    int x = w - y;
    // map N to Z
    return x % 2 == 0 ? x / 2 : -(x + 1) / 2;
}

int pi1(int c) {
    // map N to N^2 using inverse Cantor pairing function
    int w = floor((sqrt(8 * c + 1) - 1) / 2);
    int t = (w * w + w) / 2;
    int y = c - t;
    // map N to Z
    return y % 2 == 0 ? y / 2 : -(y + 1) / 2;
}

struct Direcetion {
    int check;
    int x;
    int y;
};


TYPE round(TYPE& inp, std::list<Direcetion> directions) {
    std::set<int> elves;
    for (auto& c : inp) {
        elves.insert(pair(c));
    }
    std::map<int, std::vector<Coordinates> > elves_map;
    for (auto& c : inp) {
        int count = 0;
        for (int j = -1; j <= 1; j++) {
            for (int i = -1; i <= 1; i++) {
                if (i == 0 && j == 0)
                    continue;
                Coordinates c_ = {
                    .x = c.x + i,
                    .y = c.y + j
                };
                count <<= 1;
                if (elves.find(pair(c_)) != elves.end())
                    count |= 1;
            }
        }
        Coordinates c_ = {
            .x = c.x,
            .y = c.y
        };
        // 0b11111111
        // NW N NE W E SW S SE
        if (count != 0) {
            for (auto& dir : directions) {
                if ((count & dir.check) == 0) {
                    c_.x += dir.x;
                    c_.y += dir.y;
                    break;
                }
            }
        }
        elves_map[pair(c_)].push_back(c);
    }
    TYPE out;
    for (auto& [key, value] : elves_map) {
        if (value.size() == 1) {
            Coordinates c = {
                .x = pi2(key),
                .y = pi1(key)
            };
            out.push_back(c);
        } else {
            for (auto& c : value) {
                out.push_back(c);
            }
        }
    }
    return out;
}

std::list<Direcetion> initialize_directions() {
    std::list<Direcetion> directions;
    Direcetion n = {
            .check = 0b11100000,
            .x = 0,
            .y = -1
    };
    directions.push_back(n);
    Direcetion s = {
            .check = 0b00000111,
            .x = 0,
            .y = 1
    };
    directions.push_back(s);
    Direcetion w = {
            .check = 0b10010100,
            .x = -1,
            .y = 0
    };
    directions.push_back(w);
    Direcetion e = {
            .check = 0b00101001,
            .x = 1,
            .y = 0
    };
    directions.push_back(e);
    return directions;
}

RETURN_TYPE part1(TYPE &inp) {
    RETURN_TYPE res = 0;

    std::list<Direcetion> directions = initialize_directions();

    for (int i = 0; i < 10; i++) {
        inp = round(inp, directions);
        directions.push_back(directions.front());
        directions.pop_front();
    }

    int min_x = INT_MAX;
    int max_x = INT_MIN;
    int min_y = INT_MAX;
    int max_y = INT_MIN;
    for (auto& c : inp) {
        min_x = std::min(min_x, c.x);
        max_x = std::max(max_x, c.x);
        min_y = std::min(min_y, c.y);
        max_y = std::max(max_y, c.y);
    }
    std::set<int> elves;
    for (auto& c : inp) {
        elves.insert(pair(c));
    }
    for (int y = min_y; y <= max_y; y++) {
        for (int x = min_x; x <= max_x; x++) {
            Coordinates c = {
                .x = x,
                .y = y
            };
            if (elves.find(pair(c)) != elves.end()) {
                std::cout << "#";
            } else {
                std::cout << ".";
                res++;
            }
        }
        std::cout << std::endl;
    }

    return res;
}


RETURN_TYPE part2(TYPE &inp) {
    RETURN_TYPE res = 0;

    std::list<Direcetion> directions = initialize_directions();

    std::set<int> prev_elves;
    for (auto& c : inp) {
        prev_elves.insert(pair(c));
    }
    while (true) {
        res++;
        inp = round(inp, directions);
        directions.push_back(directions.front());
        directions.pop_front();
        std::set<int> elves;
        for (auto& c : inp) {
            elves.insert(pair(c));
        }
        if (elves == prev_elves) {
            break;
        }
        prev_elves = elves;
    }

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
