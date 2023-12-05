//
// Created by Wollenschneider Luis on 04.12.22.
//

#include "../utils.hpp"
#include <list>

#define DAY "06"
#define YEAR "2022"

std::string parse_input(const std::string& filepath) {
    // check if path exists
    std::string input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        input = line;
    }
    file.close();
    return input;
}

int distinct(const std::string& inp, int n) {
    char* last_n = new char[n];
    int i;
    for (i = 0; i < n-1; i++) {
        last_n[i] = inp[i];
    }
    for (; i < inp.length(); i++) {
        last_n[n-1] = inp[i];
        bool found = true;
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                if (j != k && last_n[j] == last_n[k]) {
                    found = false;
                    break;
                }
            }
            if (!found) {
                break;
            }
        }
        if (found) {
            return i + 1;
        }
        for (int j = 0; j < n-1; j++) {
            last_n[j] = last_n[j+1];
        }
    }
    return -1;
}

int part1(const std::string& inp) {
    return distinct(inp, 4);
}

int part2(const std::string& inp) {
    return distinct(inp, 14);
}

int main() {
    std::string inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    std::string test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

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
