//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "09"
#define YEAR "2022"

struct Instruction {
    char direction;
    int amount;
};

struct Coordinates {
    int x;
    int y;
};

#define TYPE Instruction

std::list<TYPE> parse_input(const std::string& filepath) {
    // check if path exists
    std::list<TYPE> input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        TYPE instruction = {
            .direction = line[0],
            .amount = std::stoi(line.substr(2))
        };
        input.push_back(instruction);
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

bool follow(Coordinates& head, Coordinates& tail) {
    if (abs(head.x - tail.x) > 1) {
        tail.x += head.x > tail.x ? 1 : -1;
        if (head.y > tail.y)
            tail.y += 1;
        else if (head.y < tail.y)
            tail.y -= 1;
        return true;
    }
    if (abs(head.y - tail.y) > 1) {
        if (head.x > tail.x) {
            tail.x += 1;
        } else if (head.x < tail.x) {
            tail.x -= 1;
        }
        tail.y += head.y > tail.y ? 1 : -1;
        return true;
    }
    return false;
}


void move(std::vector<Coordinates>& path, int x, int y) {
    path[0].x += x;
    path[0].y += y;
    for (int i = 0; i < path.size() - 1; i++) {
        if (!follow(path[i], path[i + 1]))
            break;
    }
}

int solve(std::list<TYPE> inp, int n) {
    std::set<int> visited;

    std::vector<Coordinates> path;
    for (int i = 0; i < n; i++) {
        Coordinates c = {0, 0};
        path.push_back(c);
    }

    visited.insert(pair(path[n - 1]));
    for (const TYPE& instruction : inp) {
        for (int i = 0; i < instruction.amount; i++) {
            switch (instruction.direction) {
                case 'U':
                    move(path, 0, 1);
                    break;
                case 'D':
                    move(path, 0, -1);
                    break;
                case 'L':
                    move(path, -1, 0);
                    break;
                case 'R':
                    move(path, 1, 0);
                    break;
            }
            visited.insert(pair(path[n - 1]));
        }
    }

    return visited.size();
}

int part1(const std::list<TYPE>& inp) {
    return solve(inp, 2);
}

int part2(const std::list<TYPE>& inp) {
    return solve(inp, 10);
}

int main() {
    std::list<TYPE> inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    std::list<TYPE> test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

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
    tried.insert(2442);
    tried_before(res, tried);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
