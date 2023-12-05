//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"
#include <list>

#define DAY "11"
#define YEAR "2022"

struct Monkey {
    std::list<long> worry;
    char op; // '+' or '-'
    bool self;
    int value;
    int test;
    int success;
    int fail;
    int inspections;
};

#define TYPE Monkey

std::vector<TYPE> parse_input(const std::string& filepath) {
    // check if path exists
    std::vector<TYPE> input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    Monkey monkey;
    monkey.inspections = 0;
    while (std::getline(file, line)) {
        if (line.empty()) {
            input.push_back(monkey);
            monkey = Monkey();
            monkey.inspections = 0;
            continue;
        }
        std::string op = line.substr(0, line.find(':'));
        if (op == "  Starting items") {
            std::string w = line.substr(line.find(':') + 1);
            while (!w.empty()) {
                int i = w.find(',');
                if (i == -1) {
                    monkey.worry.push_back(std::stoi(w));
                    break;
                }
                monkey.worry.push_back(std::stoi(w.substr(0, i)));
                w = w.substr(i + 1);
            }
        } else if (op == "  Operation") {
            monkey.op = line[line.find("old") + 4];
            std::string s = line.substr(line.find(monkey.op) + 1);
            if (s.find("old") != -1) {
                monkey.self = true;
                monkey.value = 0;
            } else {
                monkey.self = false;
                monkey.value = std::stoi(s);
            }
        } else if (op == "  Test") {
            monkey.test = std::stoi(line.substr(line.find("by") + 3));
        } else if (op == "    If true") {
            monkey.success = std::stoi(line.substr(line.find("monkey") + 7));
        } else if (op == "    If false") {
            monkey.fail = std::stoi(line.substr(line.find("monkey") + 7));
        }
    }
    input.push_back(monkey);
    file.close();
    return input;
}

long long part1(std::vector<TYPE>& inp) {
    for (int i = 0; i < 20; i++) {
        for (TYPE& monkey : inp) {
            while (!monkey.worry.empty()) {
                long item = monkey.worry.front();
                monkey.worry.pop_front();
                if (monkey.op == '+') {
                    item += monkey.self ? item : monkey.value;
                } else {
                    item *= monkey.self ? item : monkey.value;
                }
                item /= 3;
                if (item % monkey.test == 0) {
                    inp[monkey.success].worry.push_back(item);
                } else {
                    inp[monkey.fail].worry.push_back(item);
                }
                monkey.inspections++;
            }
        }
    }

    long long max1 = 0;
    long long max2 = 0;
    for (const TYPE& monkey : inp) {
        if (monkey.inspections > max1) {
            max2 = max1;
            max1 = monkey.inspections;
        } else if (monkey.inspections > max2) {
            max2 = monkey.inspections;
        }
    }

    return max1 * max2;
}

long long part2(std::vector<TYPE>& inp) {
    int mod = 1;
    for (TYPE& monkey : inp) {
        mod *= monkey.test;
    }

    for (int i = 0; i < 10000; i++) {
        for (TYPE& monkey : inp) {
            while (!monkey.worry.empty()) {
                long item = monkey.worry.front();
                monkey.worry.pop_front();
                if (monkey.op == '+') {
                    item += monkey.self ? item : monkey.value;
                } else {
                    item *= monkey.self ? item : monkey.value;
                }
                item %= mod;
                if (item % monkey.test == 0) {
                    inp[monkey.success].worry.push_back(item);
                } else {
                    inp[monkey.fail].worry.push_back(item);
                }
                monkey.inspections++;
            }
        }
    }

    long long max1 = 0;
    long long max2 = 0;
    for (const TYPE& monkey : inp) {
        if (monkey.inspections > max1) {
            max2 = max1;
            max1 = monkey.inspections;
        } else if (monkey.inspections > max2) {
            max2 = monkey.inspections;
        }
    }

    return max1 * max2;
}

int main() {
    std::vector<TYPE> inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    std::vector<TYPE> test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    long long expected_result_part1 = get_expected_result<long long>(YEAR "/tests/results/day_" DAY "_1.txt");

    long long res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    long long expected_result_part2 = get_expected_result<long long>(YEAR "/tests/results/day_" DAY "_2.txt");

    inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
