//
// Created by Wollenschneider Luis on 04.12.22.
//

#include "../utils.hpp"
#include <list>
#include <stack>
#include <tuple>
#include <array>
#include <vector>

#define DAY "05"
#define YEAR "2022"

struct Steps {
    int amount;
    int from;
    int to;
};

struct Tuple {
    std::list<Steps>* steps;
    std::vector<std::stack<char> >* stacks;
};

#define TYPE Steps

Tuple* parse_input(const std::string& filepath) {
    // check if path exists
    std::list<TYPE> input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return nullptr;
    }
    std::string line;
    std::list<std::string> lines;
    while (std::getline(file, line)) {
        if (line.empty()) {
            break;
        }
        lines.push_front(line);
    }
    int i = 0;
    std::string ll = lines.front();
    int n = std::stoi(ll.substr(ll.find_last_of(' ') + 1));
    std::vector<std::stack<char> > s;
    s.resize(n);
    for (std::string l : lines) {
        if (i != 0) {
            for (int j = 0; j < l.size(); j++) {
                if (l[j] == ' ' || l[j] == '[' || l[j] == ']') {
                    continue;
                }
                s[(j - 1) / 4].push(l[j]);
            }
        }
        i++;
    }

    while (std::getline(file, line)) {
        // 1 from 2 to 1
        std::string s1 = line.substr(line.find(' ') + 1);
        int amount = std::stoi(s1.substr(0, s1.find(' ')));
        // from 2 to 1
        std::string s2 = s1.substr(s1.find(' ') + 1);
        // 2 to 1
        std::string s3 = s2.substr(s2.find(' ') + 1);
        int from = std::stoi(s3.substr(0, s3.find(' ')));
        // to 1
        std::string s4 = s3.substr(s3.find(' ') + 1);
        // 1
        std::string s5 = s4.substr(s4.find(' ') + 1);
        int to = std::stoi(s5.substr(0, s5.find(' ')));
        Steps steps = {
            .amount = amount,
            .from = from,
            .to = to
        };
        input.push_back(steps);
    }
    file.close();
    // create tuple on heap
    auto* tuple = new Tuple;
    tuple->steps = new std::list<Steps>(input);
    tuple->stacks = new std::vector<std::stack<char> >(s);
    return tuple;
}

std::string part1(Tuple inp) {
    std::string res;

    for (const TYPE& steps : *inp.steps) {
        for (int i = 0; i < steps.amount; i++) {
            char c = (*inp.stacks)[steps.from - 1].top();
            (*inp.stacks)[steps.from - 1].pop();
            (*inp.stacks)[steps.to - 1].push(c);
        }
    }

    for (auto & i : *inp.stacks) {
        res += i.top();
    }

    return res;
}

std::string part2(Tuple inp) {
    std::string res;

    for (const TYPE& steps : *inp.steps) {
        std::stack<char> s;
        for (int i = 0; i < steps.amount; i++) {
            s.push((*inp.stacks)[steps.from - 1].top());
            (*inp.stacks)[steps.from - 1].pop();
        }
        while (!s.empty()) {
            (*inp.stacks)[steps.to - 1].push(s.top());
            s.pop();
        }
    }

    for (auto & i : *inp.stacks) {
        res += i.top();
    }

    return res;
}

int main() {
    Tuple* inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    Tuple* test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    std::string expected_result_part1 = get_expected_result(YEAR "/tests/results/day_" DAY "_1.txt");

    std::string res = part1(*test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(*inp);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    std::cout << std::endl;
    std::string expected_result_part2 = get_expected_result(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(*test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(*inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
