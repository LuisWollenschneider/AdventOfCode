//
// Created by Wollenschneider Luis on 04.12.22.
//

#include "../utils.hpp"
#include <list>

#define DAY "04"
#define YEAR "2022"

struct Ranges {
    int min1;
    int max1;
    int min2;
    int max2;
};

#define TYPE Ranges

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
        unsigned long i = line.find(',');
        std::string range1 = line.substr(0, i);
        std::string range2 = line.substr(i + 1);
        TYPE ranges = {
            .min1 = std::stoi(range1.substr(0, range1.find('-'))),
            .max1 = std::stoi(range1.substr(range1.find('-') + 1)),
            .min2 = std::stoi(range2.substr(0, range2.find('-'))),
            .max2 = std::stoi(range2.substr(range2.find('-') + 1))
        };
        input.push_back(ranges);
    }
    file.close();
    return input;
}

int part1(const std::list<TYPE>& inp) {
    int res = 0;
    for (const TYPE& ranges : inp) {
        if (ranges.min1 >= ranges.min2 && ranges.max1 <= ranges.max2
            || ranges.min2 >= ranges.min1 && ranges.max2 <= ranges.max1)
            res += 1;
    }
    return res;
}

int part2(const std::list<TYPE>& inp) {
    int res = 0;
    for (const TYPE& ranges : inp) {
        if (!(ranges.max1 < ranges.min2 || ranges.max2 < ranges.min1))
            res += 1;
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
