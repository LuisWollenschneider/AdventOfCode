//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "21"
#define YEAR "2022"
#define RETURN_TYPE long long int

struct Operation {
    char op;
    std::string arg1;
    std::string arg2;
    RETURN_TYPE res;
};

#define TYPE std::map<std::string, Operation>

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
        Operation op;
        std::string name = line.substr(0, line.find(':'));
        line = line.substr(line.find(':') + 2);
        if (line.length() == 11) {
            op.op = line[5];
            op.arg1 = line.substr(0, 4);
            op.arg2 = line.substr(7, 4);
            op.res = -1;
        } else {
            op.op = 0;
            op.arg1 = "";
            op.arg2 = "";
            op.res = std::stoi(line);
        }
        input[name] = op;
    }
    file.close();
    return input;
}

RETURN_TYPE calculate(TYPE &inp, const std::string& ins) {
    if (inp[ins].res != -1) {
        return inp[ins].res;
    }
    RETURN_TYPE a = calculate(inp, inp[ins].arg1);
    RETURN_TYPE b = calculate(inp, inp[ins].arg2);
    RETURN_TYPE res = 0;
    switch (inp[ins].op) {
        case '+': {
            res = a + b;
            break;
        }
        case '*': {
            res = a * b;
            break;
        }
        case '-': {
            res = a - b;
            break;
        }
        case '/': {
            res = a / b;
            break;
        }
        case '=' : {
            res = a == b;
            break;
        }
    }
    return res;
}


RETURN_TYPE part1(TYPE &inp) {
    return calculate(inp, "root");
}

RETURN_TYPE pre_compute(TYPE &inp, const std::string& ins) {
    if (ins == "humn") {
        return -1;
    }
    if (inp[ins].res != -1) {
        return inp[ins].res;
    }
    RETURN_TYPE a = pre_compute(inp, inp[ins].arg1);
    RETURN_TYPE b = pre_compute(inp, inp[ins].arg2);
    if (a == -1 || b == -1) {
        return -1;
    }
    RETURN_TYPE res = 0;
    switch (inp[ins].op) {
        case '+': {
            res = a + b;
            break;
        }
        case '*': {
            res = a * b;
            break;
        }
        case '-': {
            res = a - b;
            break;
        }
        case '/': {
            res = a / b;
            break;
        }
        case '=' : {
            res = a == b;
            break;
        }
    }
    inp[ins].res = res;
    return res;
}

RETURN_TYPE backtrace(TYPE &inp, const std::string& ins, RETURN_TYPE res) {
    if (ins == "humn") {
        return res;
    }
    RETURN_TYPE a = inp[inp[ins].arg1].res;
    RETURN_TYPE b = inp[inp[ins].arg2].res;
    std::string instruction;
    RETURN_TYPE res2;
    if (a == -1) {
        instruction = inp[ins].arg1;
        switch (inp[ins].op) {
            case '+': {
                // res = a + b;
                res2 = res - b;
                break;
            }
            case '*': {
                // res = a * b;
                res2 = res / b;
                break;
            }
            case '-': {
                // res = a - b;
                res2 = res + b;
                break;
            }
            case '/': {
                // res = a / b;
                res2 = res * b;
                break;
            }
            case '=' : {
                res2 = b;
                break;
            }
        }
    } else if (b == -1) {
        instruction = inp[ins].arg2;
        switch (inp[ins].op) {
            case '+': {
                // res = a + b;
                res2 = res - a;
                break;
            }
            case '*': {
                // res = a * b;
                res2 = res / a;
                break;
            }
            case '-': {
                // res = a - b;
                res2 = a - res;
                break;
            }
            case '/': {
                // res = a / b;
                res2 = a / res;
                break;
            }
            case '=' : {
                res2 = a;
                break;
            }
        }
    } else {
        std::cout << "Error" << std::endl;
        exit(1);
    }
    return backtrace(inp, instruction, res2);
}

RETURN_TYPE part2(TYPE &inp) {
    inp["root"].op = '=';
    pre_compute(inp, "root");
    inp["humn"].res = -1;

    return backtrace(inp, "root", 1);
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    auto expected_result_part1 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_1.txt");

    RETURN_TYPE res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::set<RETURN_TYPE> tried;
    tried.insert(-393342880);
    tried_before(res, tried);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    auto expected_result_part2 = get_expected_result<RETURN_TYPE>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<RETURN_TYPE> tried2;
    tried2.insert(10708574);
    tried_before(res, tried2);
    std::cout << COLOR_RED "Written in Python, due to overflow!" COLOR_RESET << std::endl;
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
