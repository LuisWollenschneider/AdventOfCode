//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"
#include <list>

#define DAY "03"
#define YEAR "2022"

struct Backpack {
    std::string content;
    std::string first_half;
    std::string second_half;
};

#define TYPE Backpack

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
        Backpack backpack = {
            .content = line,
            .first_half = line.substr(0, line.size() / 2),
            .second_half = line.substr(line.size() / 2, line.size() / 2)
        };
        input.push_back(backpack);
    }
    file.close();
    return input;
}

int part1(const std::list<TYPE>& inp) {
    int res = 0;
    for (const Backpack& backpack : inp) {
        bool found = false;
        for (int i = 0; i < backpack.first_half.size(); i++) {
            for (int j = 0; j < backpack.second_half.size(); j++) {
                if (backpack.first_half[i] == backpack.second_half[j]) {
                    if (backpack.first_half[i] >= 'a' && backpack.first_half[i] <= 'z') {
                        res += backpack.first_half[i] - 'a' + 1;
                    } else {
                        res += backpack.first_half[i] - 'A' + 1 + 26;
                    }
                    found = true;
                    break;
                }
            }
            if (found) {
                break;
            }
        }
    }
    return res;
}

int part2(const std::list<TYPE>& inp) {
    int res = 0;
    for (int i = 0; i < inp.size(); i += 3) {
        const Backpack& backpack1 = *std::next(inp.begin(), i);
        const Backpack& backpack2 = *std::next(inp.begin(), i + 1);
        const Backpack& backpack3 = *std::next(inp.begin(), i + 2);
        bool found = false;
        for (char j : backpack1.content) {
            for (char k : backpack2.content) {
                if (j != k) {
                    continue;
                }
                for (char l : backpack3.content) {
                    if (k != l) {
                        continue;
                    }
                    if (j >= 'a' && j <= 'z') {
                        res += j - 'a' + 1;
                    } else {
                        res += j - 'A' + 1 + 26;
                    }
                    found = true;
                    break;
                }
                if (found) {
                    break;
                }
            }
            if (found) {
                break;
            }
        }
    }
    return res;
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
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
