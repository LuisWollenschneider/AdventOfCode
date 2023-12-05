//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.h"
#include "math.h"

#define DAY "25"
#define YEAR "2022"
#define RETURN_TYPE std::string

#define TYPE std::vector<std::string>

TYPE parse_input(const std::string &filepath) {
    // check if path exists
    TYPE input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        input.push_back(line);
    }
    file.close();
    return input;
}

long long convert(std::string s) {
    long long n = 0;
    for (char c : s) {
        n *= 5;
        switch (c) {
            case '-': {
                n += -1;
                break;
            }
            case '=': {
                n += -2;
                break;
            }
            default: {
                n += c - '0';
                break;
            }
        }
    }
    return n;
}

std::string convert(long long n) {
    std::string s;
    int pow5 = 1;
    while (n != 0) {
        for (int i = -2; i <= 2; i++) {
            if ((n - i * (int)pow(5, pow5 - 1)) % (int)pow(5, pow5) == 0) {
                switch (i) {
                    case -2: {
                        s += '=';
                        break;
                    }
                    case -1: {
                        s += '-';
                        break;
                    }
                    default: {
                        s += (char)('0' + i);
                        break;
                    }
                }
                n -= i * (int)pow(5, pow5 - 1);
                break;
            }
        }
        pow5++;
    }
    return std::reverse(s.begin(), s.end()), s;
}

RETURN_TYPE part1(TYPE& inp) {
    long long res = 0;

    for (std::string s : inp) {
        res += convert(s);
    }
    std::cout << res << std::endl;
    return convert(res);
}


RETURN_TYPE part2(TYPE& inp) {
    int res = 0;

    return "";
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    auto expected_result_part1 = get_expected_result(YEAR "/tests/results/day_" DAY "_1.txt");

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
    auto expected_result_part2 = get_expected_result(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<RETURN_TYPE> tried2;
    tried_before(res, tried2);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
