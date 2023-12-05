//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "18"
#define YEAR "2022"

struct Coordinate {
    int x;
    int y;
    int z;
};

#define TYPE std::vector<Coordinate>

TYPE parse_input(const std::string& filepath) {
    // check if path exists
    TYPE input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        Coordinate c = {
            std::stoi(line),
            std::stoi(line.substr(line.find(',') + 1)),
            std::stoi(line.substr(line.find_last_of(',') + 1))
        };
        input.push_back(c);
    }
    file.close();
    return input;
}

int pair3(int x, int y, int z) {
    // map coordinates to a unique number in N
    // map N^2 to N using Cantor pairing function
    return (x << 12) + (y << 6) + z;
}

int pair2(int x, int y) {
    // map coordinates to a unique number in N
    // map N^2 to N using Cantor pairing function
    return (x << 18) + y;
}

std::set<int> get_sides(int x, int y, int z) {
    std::set<int> sides;
    for (int x2 = 0; x2 < 2; x2++) {
        sides.insert(pair2(pair3(x + x2, y, z), pair3(x + x2, y + 1, z + 1)));
    }
    for (int y2 = 0; y2 < 2; y2++) {
        sides.insert(pair2(pair3(x, y + y2, z), pair3(x + 1, y + y2, z + 1)));
    }
    for (int z2 = 0; z2 < 2; z2++) {
        sides.insert(pair2(pair3(x, y, z + z2), pair3(x + 1, y + 1, z2 + z)));
    }
    return sides;
}

int part1(TYPE& inp) {
    std::set<int> sides;
    std::set<int> duplicates;
    int a;

    for (auto& c : inp) {
        for (auto& s : get_sides(c.x, c.y, c.z)) {
            if (sides.find(s) != sides.end()) {
                duplicates.insert(s);
            }
            sides.insert(s);
        }
    }

    return sides.size() - duplicates.size();
}

void get_outside(int x, int y, int z, std::set<int>* outside, std::set<int>* inside) {
    if (x < -1 || y < -1 || z < -1 || x > 21 || y > 21 || z > 21) {
        return;
    }

    bool visited = true;
    bool inside_visited = true;
    std::set<int> sides = get_sides(x, y, z);
    for (auto& s : sides) {
        if (!visited && !inside_visited) {
            break;
        }
        if (outside->find(s) == outside->end()) {
            visited = false;
        }
        if (inside->find(s) == inside->end()) {
            inside_visited = false;
        }
    }
    if (visited || inside_visited) {
        return;
    }

    for (auto& s : sides) {
        outside->insert(s);
    }

    get_outside(x + 1, y, z, outside, inside);
    get_outside(x - 1, y, z, outside, inside);
    get_outside(x, y + 1, z, outside, inside);
    get_outside(x, y - 1, z, outside, inside);
    get_outside(x, y, z + 1, outside, inside);
    get_outside(x, y, z - 1, outside, inside);
}

int part2(TYPE& inp) {
    std::set<int> sides;
    std::set<int> duplicates;

    for (auto& c : inp) {
        for (auto& s : get_sides(c.x, c.y, c.z)) {
            sides.insert(s);
        }
    }
    
    std::set<int> sides2;
    get_outside(0, 0, 0, &sides2, &sides);

    int c = 0;
    for (auto& s : sides2) {
        if (sides.find(s) != sides.end()) {
            c++;
        }
    }

    return c;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    int expected_result_part1 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_1.txt");

    int res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    int expected_result_part2 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<int> tried;
    tried.insert(2058);
    tried_before(res, tried);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
