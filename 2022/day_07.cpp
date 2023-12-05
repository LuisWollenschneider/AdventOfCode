//
// Created by Wollenschneider Luis on 04.12.22.
//

#include "../utils.hpp"
#include <vector>

#define DAY "07"
#define YEAR "2022"

struct File {
    std::string name;
    int size;
};

struct Directory {
    std::string name;
    std::vector<Directory> subdirectories;
    std::vector<File> files;
};

#define TYPE Directory

TYPE parse_input(const std::string& filepath) {
    // check if path exists
    TYPE input = {
        .name = "/",
        .subdirectories = *new std::vector<TYPE>(),
        .files = *new std::vector<File>()
    };
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    std::stack<TYPE*> stack;
    stack.push(&input);
    while (std::getline(file, line)) {
        std::string size = line.substr(0, line.find(" "));
        std::string name = line.substr(line.find(" ") + 1);
        if (size == "$") {
            // command
            if (name == "ls") {
                continue;
            }
            std::string dst = name.substr(name.find(" ") + 1);
            if (dst == "/") {
                stack = std::stack<TYPE*>();
                stack.push(&input);
            } else if (dst == "..") {
                stack.pop();
            } else {
                for (TYPE& dir : stack.top()->subdirectories) {
                    if (dir.name == dst) {
                        stack.push(&dir);
                        break;
                    }
                }
            }
            continue;
        }
        if (size == "dir") {
            // directory
            TYPE dir = {
                .name = name,
                .subdirectories = *new std::vector<TYPE>(),
                .files = *new std::vector<File>()
            };
            stack.top()->subdirectories.push_back(dir);
            continue;
        }
        File f = {
            .name = name,
            .size = std::stoi(size)
        };
        stack.top()->files.push_back(f);
    }
    file.close();
    return input;
}

int size(const TYPE& inp) {
    int s = 0;
    for (File f : inp.files) {
        s += f.size;
    }
    for (TYPE d : inp.subdirectories) {
        s += size(d);
    }
    return s;
}

int dir_size(const TYPE& dir, const int n) {
    int s = 0;
    int directory_size = size(dir);
    if (directory_size <= n) {
        s += directory_size;
    }
    for (TYPE d : dir.subdirectories) {
        s += dir_size(d, n);
    }
    return s;
}

int part1(const TYPE& inp) {
    return dir_size(inp, 100000);
}

int min_size(const TYPE& dir, const int n) {
    int s = INT_MAX;
    int directory_size = size(dir);
    if (directory_size >= n) {
        s = std::min(s, directory_size);
    }
    for (TYPE d : dir.subdirectories) {
        s = std::min(s, min_size(d, n));
    }
    return s;
}

int part2(const TYPE& inp) {
    int s = size(inp);
    int req = -40000000 + s;

    return min_size(inp, req);
}

int main() {
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

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
