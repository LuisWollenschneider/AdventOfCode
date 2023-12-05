//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "20"
#define YEAR "2022"
#define RETURN_TYPE int

#define TYPE std::vector<int>

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
        input.push_back(std::stoi(line));
    }
    file.close();
    return input;
}

struct V {
    int value;
    int original_index;
    int index;
};


RETURN_TYPE part1(TYPE &inp) {
    RETURN_TYPE res = 0;

    // idx to val
    std::map<int, V*> original;
    // mixed
    std::map<int, V*> mixed;

    int s = 0;
    for (int i = 0; i < inp.size(); i++) {
        V* v = new V();
        v->value = inp[i];
        v->original_index = i;
        v->index = i;
        original[i] = v;
        mixed[i] = v;
        s = i + 1;
    }

    for (int i = 0; i < inp.size(); i++) {
        V* v = original[i];
        int index = v->index;
        int new_index = index + v->value;
        if (new_index >= s) {
            new_index = (new_index + 1) % s;
        } else if (new_index < 0) {
            new_index = (new_index + s * 10 - 1) % s;
        }
        if (new_index == 0) {
            new_index = s - 1;
        }

        for (int j = index + 1; j <= new_index; j++) {
            mixed[j - 1] = mixed[j];
            mixed[j - 1]->index--;
            // assert(i-1 == mixed[i-1]->index);
        }
        for (int j = index - 1; j >= new_index; j--) {
            mixed[j + 1] = mixed[j];
            mixed[j + 1]->index++;
            // assert(j+1 == mixed[j+1]->index);
        }
        mixed[new_index] = v;

        /*
        std::cout << v->value << " moved from " << index << " to " << new_index << std::endl;
        for (int j = 0; j < s; j++) {
            std::cout << mixed[j]->value << ", ";
        }
        std::cout << std::endl;
        std::cout << std::endl;
        */
    }

    int zero = 0;
    for (int i = 0; i < s; i++) {
        if (mixed[i]->value == 0) {
            zero = i;
            break;
        }
    }
    std::cout << "zero: " << zero << std::endl;
    for (int i = 1; i <= 3; i++) {
        int idx = (zero + i * 1000) % s;
        std::cout << "Index: " << idx << " Val: " << mixed[idx]->value << std::endl;
        res += mixed[idx]->value;
    }

    return res;
}

RETURN_TYPE part2(TYPE &inp) {
    RETURN_TYPE res = 1;

    return res;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    std::cout << COLOR_RED "Written in Python!" COLOR_RESET << std::endl;

    auto expected_result_part1 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_1.txt");

    RETURN_TYPE res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::set<RETURN_TYPE> tried;
    tried.insert(2713);
    tried_before(res, tried);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    RETURN_TYPE expected_result_part2 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<RETURN_TYPE> tried2;
    tried_before(res, tried2);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
