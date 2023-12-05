//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"
#include <list>
#include <vector>

#define DAY "08"
#define YEAR "2022"

#define TYPE std::string

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
        input.push_back(line);
    }
    file.close();
    return input;
}

bool check_tree(const std::vector<TYPE>& trees, int x, int y) {
    if (x == 0 || x == trees.size() - 1) {
        return true;
    }
    if (y == 0 || y == trees[0].size() - 1) {
        return true;
    }
    int t = trees[x][y] - '0';
    bool above = true, below = true, left = true, right = true;
    for (int i = 0; i < trees.size(); i++) {
        if (i == x)
            continue;
        int t2 = trees[i][y] - '0';
        if (t2 >= t) {
            if (i < x) {
                left = false;
                i = x;
            } else {
                right = false;
                break;
            }
        }
    }
    for (int j = 0; j < trees[x].size(); j++) {
        if (j == y)
            continue;
        int t2 = trees[x][j] - '0';
        if (t2 >= t) {
            if (j < y) {
                above = false;
                j = y;
            } else {
                below = false;
                break;
            }
        }
    }
    return above || below || left || right;
}

int part1(const std::vector<TYPE>& inp) {
    int res = 0;

    for (int x = 0; x < inp.size(); x++) {
        for (int y = 0; y < inp[x].size(); y++) {
            if (check_tree(inp, x, y))
                res += 1;
        }
    }

    return res;
}

int tree_score(const std::vector<TYPE>& trees, int x, int y) {
    if (x == 0 || x == trees.size() - 1) {
        return 0;
    }
    if (y == 0 || y == trees[0].size() - 1) {
        return 0;
    }
    int t = trees[x][y] - '0';
    int score = 1;
    int i;
    for (i = x - 1; i >= 0; i--) {
        int t2 = trees[i][y] - '0';
        if (t2 >= t) {
            i--;
            break;
        }
    }
    score *= x - (i + 1);
    for (i = x + 1; i < trees.size(); i++) {
        int t2 = trees[i][y] - '0';
        if (t2 >= t) {
            i++;
            break;
        }
    }
    score *= i - x - 1;
    for (i = y - 1; i >= 0; i--) {
        int t2 = trees[x][i] - '0';
        if (t2 >= t) {
            i--;
            break;
        }
    }
    score *= y - (i + 1);
    for (i = y + 1; i < trees[x].size(); i++) {
        int t2 = trees[x][i] - '0';
        if (t2 >= t) {
            i++;
            break;
        }
    }
    score *= i - y - 1;
    return score;
}

int part2(const std::vector<TYPE>& inp) {
    int res = 0;

    for (int x = 0; x < inp.size(); x++) {
        for (int y = 0; y < inp[x].size(); y++) {
            res = std::max(tree_score(inp, x, y), res);
        }
    }

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
    int expected_result_part2 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
