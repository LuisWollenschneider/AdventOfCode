//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "13"
#define YEAR "2022"

struct list_or_int;

struct Tuple {
    list_or_int *first;
    list_or_int *second;
};

struct list_or_int {
    std::vector<list_or_int *> *list;
    int integer;
};

#define TYPE std::vector<Tuple*>*

list_or_int *parse_line(std::string line) {
    auto *l = new list_or_int;
    l->integer = -1;
    l->list = new std::vector<list_or_int *>();
    line = line.substr(1);
    std::stack<list_or_int *> stack;
    stack.push(l);
    while (!line.empty()) {
        if (line[0] == '[') {
            auto *l2 = new list_or_int();
            l2->integer = -1;
            l2->list = new std::vector<list_or_int *>();
            stack.top()->list->push_back(l2);
            stack.push(stack.top()->list->back());
            line = line.substr(1);
        } else if (line[0] == ']') {
            stack.pop();
            line = line.substr(1);
        } else if (line[0] == ',') {
            line = line.substr(1);
        } else {
            auto *l2 = new list_or_int();
            l2->integer = std::stoi(line);
            l2->list = nullptr;
            stack.top()->list->push_back(l2);
            line = line.substr(std::to_string(l2->integer).size());
        }
    }
    return l;
}

TYPE parse_input(const std::string &filepath) {
    // check if path exists
    TYPE input = new std::vector<Tuple *>();
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    auto *tuple = new Tuple();
    tuple->first = nullptr;
    tuple->second = nullptr;
    input->push_back(tuple);
    while (std::getline(file, line)) {
        if (line.empty()) {
            Tuple *tp = new Tuple();
            tp->first = nullptr;
            tp->second = nullptr;
            input->push_back(tp);
            continue;
        }

        if (input->back()->first == nullptr) {
            input->back()->first = parse_line(line);
        } else {
            input->back()->second = parse_line(line);
        }
    }
    file.close();
    return input;
}

int cmp(list_or_int *a, list_or_int *b) {
    if (a->integer != -1 && b->integer != -1) {
        return b->integer - a->integer;
    }
    if (a->integer != -1) {
        auto *l = new list_or_int();
        l->integer = -1;
        l->list = new std::vector<list_or_int *>();
        l->list->push_back(a);
        return cmp(l, b);
    }
    if (b->integer != -1) {
        auto *l = new list_or_int();
        l->integer = -1;
        l->list = new std::vector<list_or_int *>();
        l->list->push_back(b);
        return cmp(a, l);
    }
    for (int i = 0; i < a->list->size(); i++) {
        if (i >= b->list->size()) {
            return -1;
        }
        int res = cmp(a->list->at(i), b->list->at(i));
        if (res != 0) {
            return res;
        }
    }
    if (a->list->size() < b->list->size()) {
        return 1;
    }
    return 0;
}

int part1(TYPE&inp) {
    int res = 0;

    int i = 1;
    for (Tuple *t: *inp) {
        if (cmp(t->first, t->second) > 0) {
            res += i;
        }
        i++;
    }

    return res;
}

int part2(TYPE&inp) {
    int res = 1;

    list_or_int* sep1 = parse_line("[[2]]");
    list_or_int* sep2 = parse_line("[[6]]");

    auto* a = new std::vector<list_or_int*>();
    a->push_back(sep1);
    a->push_back(sep2);
    for (Tuple *t : *inp) {
        a->push_back(t->first);
        a->push_back(t->second);
    }

    for (int i = 0; i < a->size(); i++) {
        for (int j = i + 1; j < a->size(); j++) {
            if (cmp(a->at(i), a->at(j)) > 0) {
                list_or_int* tmp = a->at(i);
                a->at(i) = a->at(j);
                a->at(j) = tmp;
            }
        }
    }

    for (int i = 0; i < a->size(); i++) {
        if (a->at(i) == sep1) {
            res *= a->size() - i;
        }
        if (a->at(i) == sep2) {
            res *= a->size() - i;
        }
    }

    return res;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

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
