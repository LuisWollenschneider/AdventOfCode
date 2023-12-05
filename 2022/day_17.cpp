//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "17"
#define YEAR "2022"

struct Coordinate {
    long long int x;
    long long int y;
};

#define TYPE std::string

TYPE parse_input(const std::string& filepath) {
    // check if path exists
    TYPE input;
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "File not found" << std::endl;
        return input;
    }
    std::string line;
    while (std::getline(file, line)) {
        input += line;
    }
    file.close();
    return input;
}

long pair(const Coordinate c) {
    // map coordinates to a unique number in N
    // map N^2 to N using Cantor pairing function
    return c.y * 7 + c.x;
}

std::vector<Coordinate> get_rock(long idx, long height) {
    std::vector<Coordinate> rock;
    switch (idx % 5) {
        case 0: {
            // ####
            for (int i = 2; i < 6; i++) {
                Coordinate c1 = {i, height};
                rock.push_back(c1);
            }
            break;
        }
        case 1: {
            // .#.
            // ###
            // .#.
            for (int i = 2; i < 5; i++) {
                Coordinate c2 = {i, height + 1};
                rock.push_back(c2);
            }
            Coordinate c3 = {3, height};
            rock.push_back(c3);
            Coordinate c4 = {3, height + 2};
            rock.push_back(c4);
            break;
        }
        case 2: {
            // ..#
            // ..#
            // ###
            for (int i = 2; i < 5; i++) {
                Coordinate c5 = {i, height};
                rock.push_back(c5);
            }
            Coordinate c6 = {4, height + 1};
            rock.push_back(c6);
            Coordinate c7 = {4, height + 2};
            rock.push_back(c7);
            break;
        }
        case 3: {
            // #
            // #
            // #
            // #
            for (int i = 0; i < 4; i++) {
                Coordinate c8 = {2, height + i};
                rock.push_back(c8);
            }
            break;
        }
        case 4: {
            // ##
            // ##
            for (int i = 0; i < 2; i++) {
                for (int j = 0; j < 2; j++) {
                    Coordinate c9 = {2 + i, height + j};
                    rock.push_back(c9);
                }
            }
            break;
        }
    }
    return rock;
}

long long int solve(TYPE& inp, long y) {
    std::set<long long int> rocks;
    for (int j = 0; j < 7; j++) {
        Coordinate c = {j, 0};
        rocks.insert(pair(c));
    }
    long long int height = 0;
    long long int rock_counter = 0;
    long long int i = 0;

    std::map<long long int, long long int> base;
    std::map<long long int, long long int> diff;
    std::map<long long int, long long int> idx;
    bool pattern_found = false;
    long cycle_height = 0;

    while (rock_counter < y) {
        std::vector<Coordinate> rock_coords = get_rock(rock_counter, height + 4);
        long k = ((i % inp.size()) << 3) + rock_counter % 5;
        if (!pattern_found) {
            if (base.find(k) != diff.end()) {
                if (diff.find(k) != diff.end()) {
                    if (diff[k] == height - base[k]) {
                        pattern_found = true;
                        std::cout << "found pattern" << std::endl;
                        std::cout << "base:   " << base[k] << std::endl;
                        std::cout << "height: " << height << std::endl;
                        std::cout << "diff:   " << diff[k] << std::endl;
                        std::cout << "idx:    " << idx[k] << std::endl;
                        std::cout << "i:      " << i % inp.size() << std::endl;
                        std::cout << "size:   " << rock_counter - idx[k] << std::endl;
                        long n = (y - rock_counter) / (rock_counter - idx[k]);
                        rock_counter += n * (rock_counter - idx[k]);
                        cycle_height = n * diff[k];
                    }
                }
                diff[k] = height - base[k];
            }
            base[k] = height;
            idx[k] = rock_counter;
        }

        rock_counter++;
        while (true) {
            char d = inp[i % inp.size()];
            i++;
            int dir;
            if (d == '<') {
                dir = -1;
            } else if (d == '>') {
                dir = 1;
            }
            std::vector<Coordinate> new_rock_coords;
            bool worked = true;
            for (Coordinate& c : rock_coords) {
                Coordinate new_c = {c.x + dir, c.y};
                if (new_c.x < 0 || new_c.x > 6) {
                    worked = false;
                    // std::cout << "Out of bounds" << std::endl;
                    break;
                }
                if (rocks.find(pair(new_c)) != rocks.end()) {
                    worked = false;
                    // std::cout << "Rock collision" << std::endl;
                    break;
                }
                new_rock_coords.push_back(new_c);
            }
            if (worked) {
                // std::cout << "Moved " << (dir == -1 ? "left" : "right") << std::endl;
                rock_coords = new_rock_coords;
            }
            new_rock_coords.clear();
            worked = true;
            for (Coordinate& c : rock_coords) {
                Coordinate new_c = {c.x, c.y - 1};
                new_rock_coords.push_back(new_c);
                if (rocks.find(pair(new_c)) != rocks.end()) {
                    worked = false;
                    break;
                }
            }
            if (worked) {
                // std::cout << "Moving down" << std::endl;
                rock_coords = new_rock_coords;
            } else {
                // std::cout << "STOPPED" << std::endl;
                for (Coordinate& c : rock_coords) {
                    height = std::max(height, c.y);
                    rocks.insert(pair(c));
                }
                break;
            }
        }
        /*
        for (int h = height; h > 0; h--) {
            std::cout << "|";
            for (int j = 0; j < 7; j++) {
                Coordinate c = {j, h};
                if (rocks.find(pair(c)) != rocks.end()) {
                    std::cout << "#";
                } else {
                    std::cout << ".";
                }
            }
            std::cout << "|" << std::endl;
        }
        std::cout << "+-------+" << std::endl;
        std::cout << std::endl;
        */
    }

    return height + cycle_height;
}

long long int part1(TYPE& inp) {
    return solve(inp, 2022);
}

long long int part2(TYPE& inp) {
    return solve(inp, 1000000000000);
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    long long int expected_result_part1 = get_expected_result<long long int>(YEAR "/tests/results/day_" DAY "_1.txt");

    long long int res = part1(test_inp);
    bool eval_res = evaluate_results(res, expected_result_part1);
    res = part1(inp);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    long long int expected_result_part2 = get_expected_result<long long int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
