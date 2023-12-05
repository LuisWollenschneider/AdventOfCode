//
// Created by Wollenschneider Luis on 02.12.22.
//

#include "../utils.hpp"
#include <list>

#define DAY "02"
#define YEAR "2022"

struct RPS {
    int opponent;
    int player;
};

#define TYPE RPS

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
        RPS rps = {
            line[0] - 'A',
            line[2] - 'X'
        };
        input.push_back(rps);
    }
    file.close();
    return input;
}

int part1(const std::list<TYPE>& inp) {
    int score = 0;
    for (const RPS& rps : inp) {
        int round = rps.player + 1;
        if (rps.opponent == rps.player) {
            // draw
            round += 3;
        } else if (rps.player == (rps.opponent + 1) % 3) {
            // win
            round += 6;
        }
        score += round;
    }
    return score;
}

int part2(const std::list<TYPE>& inp) {
    int score = 0;
    for (const RPS& rps : inp) {
        int round = 0;
        switch (rps.player) {
            case 0:
                round = (rps.opponent - 1 + 3) % 3 + 1;
                break;
            case 1:
                round = 3;
                round += rps.opponent + 1;
                break;
            case 2:
                round = 6;
                round += (rps.opponent + 1) % 3 + 1;
                break;
            default:
                break;
        }
        score += round;
    }
    return score;
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
