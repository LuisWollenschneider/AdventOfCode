//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "14"
#define YEAR "2022"

struct Coordinate {
    int x;
    int y;
};

struct Path {
    std::vector<Coordinate> coordinates;
};

#define TYPE std::vector<Path>

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
        Path path;
        while (!line.empty()) {
            std::string coord = line.substr(0, line.find("->"));
            Coordinate coordinate = {
                .x = std::stoi(coord.substr(0, coord.find(','))),
                .y = std::stoi(coord.substr(coord.find(',') + 1))
            };
            path.coordinates.push_back(coordinate);
            if (line.find("->") == std::string::npos) {
                break;
            }
            line = line.substr(line.find("->") + 2);
        }
        input.push_back(path);
    }
    file.close();
    return input;
}

int pair(const Coordinate c) {
    // map coordinates to a unique number in N
    // map Z to N / positive number -> even, negative number -> odd
    int i = c.x >= 0 ? c.x * 2 : -c.x * 2 - 1;
    int j = c.y >= 0 ? c.y * 2 : -c.y * 2 - 1;
    // map N^2 to N using Cantor pairing function
    return 0.5 * (i + j) * (i + j + 1) + j;
}



int part1(TYPE& inp) {
    int res = 0;

    std::map<int, char> map;
    int max_y = 0;

    for (Path& path : inp) {
        for (int i = 0; i < path.coordinates.size() - 1; i++) {
            Coordinate c1 = path.coordinates[i];
            max_y = std::max(max_y, c1.y);
            Coordinate c2 = path.coordinates[i + 1];
            max_y = std::max(max_y, c2.y);

            int cx = c1.x;
            int cy = c1.y;
            int x = 0;
            if (c1.x != c2.x) {
                x = c1.x < c2.x ? 1 : -1;
            }
            int y = 0;
            if (c1.y != c2.y) {
                y = c1.y < c2.y ? 1 : -1;
            }
            do {
                Coordinate c = {
                    .x = cx,
                    .y = cy
                };
                map[pair(c)] = '#';
                cx += x;
                cy += y;
            } while (cx != c2.x || cy != c2.y);
            map[pair(c2)] = '#';
        }
    }

    while (true) {
        Coordinate sand = {
            .x = 500,
            .y = 0
        };
        while (true) {
            if (sand.y > max_y) {
                return res;
            }
            sand.y++;
            if (!map.count(pair(sand))) {
                continue;
            }
            sand.x--;
            if (!map.count(pair(sand))) {
                continue;
            }
            sand.x += 2;
            if (!map.count(pair(sand))) {
                continue;
            }
            break;
        }
        sand.y--;
        sand.x--;
        map[pair(sand)] = 'o';
        res++;
    }
}

int part2(TYPE& inp) {
    int res = 0;

    std::map<int, char> map;
    int max_y = 0;

    for (Path& path : inp) {
        for (int i = 0; i < path.coordinates.size() - 1; i++) {
            Coordinate c1 = path.coordinates[i];
            max_y = std::max(max_y, c1.y);
            Coordinate c2 = path.coordinates[i + 1];
            max_y = std::max(max_y, c2.y);

            int cx = c1.x;
            int cy = c1.y;
            int x = 0;
            if (c1.x != c2.x) {
                x = c1.x < c2.x ? 1 : -1;
            }
            int y = 0;
            if (c1.y != c2.y) {
                y = c1.y < c2.y ? 1 : -1;
            }
            do {
                Coordinate c = {
                        .x = cx,
                        .y = cy
                };
                map[pair(c)] = '#';
                cx += x;
                cy += y;
            } while (cx != c2.x || cy != c2.y);
            map[pair(c2)] = '#';
        }
    }

    while (true) {
        Coordinate sand = {
            .x = 500,
            .y = 0
        };
        if (map.count(pair(sand))) {
            return res;
        }
        while (true) {
            if (sand.y == max_y + 1) {
                for (int i = -1; i < 2; i++) {
                    Coordinate c = {
                        .x = sand.x + i,
                        .y = sand.y + 1
                    };
                    map[pair(c)] = '#';
                }
            }
            sand.y++;
            if (!map.count(pair(sand))) {
                continue;
            }
            sand.x--;
            if (!map.count(pair(sand))) {
                continue;
            }
            sand.x += 2;
            if (!map.count(pair(sand))) {
                continue;
            }
            break;
        }
        sand.x--;
        sand.y--;
        map[pair(sand)] = 'o';
        res++;
    }
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

    inp = parse_input(YEAR "/inputs/day_" DAY ".txt");
    test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");

    std::cout << std::endl;
    int expected_result_part2 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
