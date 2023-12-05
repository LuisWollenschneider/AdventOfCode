//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "10"
#define YEAR "2022"

struct Instruction {
    std::string ins;
    int val;
};

#define TYPE Instruction

std::vector<TYPE> parse_input(const std::string& filepath) {
    // check if path exists
    std::vector<TYPE> input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        int v = 0;
        if (line.length() > 4) {
            v = std::stoi(line.substr(line.find(' ') + 1));
        }
        TYPE instruction = {
            .ins = line.substr(0, line.find(' ')),
            .val = v
        };
        input.push_back(instruction);
    }
    file.close();
    return input;
}

int part1(const std::vector<TYPE>& inp) {
    int res = 0;

    int reg = 1;

    int i = 1;
    for (const TYPE& instruction : inp) {
        if (instruction.ins == "noop") {
            i++;
        } else if (instruction.ins == "addx") {
            i++;
            if ((i - 20) % 40 == 0) {
                res += reg * i;
            }
            i++;
            reg += instruction.val;
        }
        if ((i - 20) % 40 == 0) {
            res += reg * i;
        }
    }

    return res;
}

int part2(const std::vector<TYPE>& inp) {
    int res = 0;

    int reg = 2;

    std::vector<std::string> out;

    int i = 0;
    for (const TYPE& instruction : inp) {
        int new_reg = reg;
        if (instruction.ins == "noop") {
            i++;
        } else if (instruction.ins == "addx") {
            i++;
            for (int j = -1; j <= 1; j++) {
                if (reg + j == i - (40 * (i / 40))) {
                    while (i / 40 >= out.size()) {
                        out.push_back("........................................");
                    }
                    out[i / 40][(i - 1) % 40] = '#';
                    break;
                }
            }
            i++;
            new_reg += instruction.val;
        }
        for (int j = -1; j <= 1; j++) {
            if (reg + j == i - (40 * (i / 40))) {
                while (i / 40 >= out.size()) {
                    out.push_back("........................................");
                }
                out[i / 40][(i - 1) % 40] = '#';
                break;
            }
        }
        reg = new_reg;
    }

    for (std::string s : out) {
        std::cout << s << std::endl;
    }
    std::cout << std::endl;

    return res;
}

int main() {
    std::vector<TYPE> inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    std::vector<TYPE> test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    int expected_result_part1 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_1.txt");

    int res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    // int expected_result_part2 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    // evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
