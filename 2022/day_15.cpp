//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "15"
#define YEAR "2022"

struct Coordinate {
    int x;
    int y;
};

struct Sensor_Beacon {
    Coordinate sensor;
    Coordinate beacon;
};

struct Range {
    int min;
    int max;
};

#define TYPE std::vector<Sensor_Beacon>

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
        // Sensor at x=13820, y=3995710: closest beacon is at x=1532002, y=3577287
        std::string sensor = line.substr(12, line.find(':') - 12);
        std::string beacon = line.substr(line.find(':') + 25);
        Coordinate s = {
            std::stoi(sensor),
            std::stoi(sensor.substr(sensor.find('=') + 1))
        };
        Coordinate b = {
            std::stoi(beacon),
            std::stoi(beacon.substr(beacon.find('=') + 1))
        };
        Sensor_Beacon sb = {s, b};
        input.push_back(sb);
    }
    file.close();
    return input;
}

long long int pair(const Coordinate c) {
    // map coordinates to a unique number in N
    // map Z to N / positive number -> even, negative number -> odd
    long long int i = c.x >= 0 ? c.x * 2 : -c.x * 2 - 1;
    long long int j = c.y >= 0 ? c.y * 2 : -c.y * 2 - 1;
    // map N^2 to N using Cantor pairing function
    return 0.5 * (i + j) * (i + j + 1) + j;
}

int distance(const Coordinate c1, const Coordinate c2) {
    return std::abs(c1.x - c2.x) + std::abs(c1.y - c2.y);
}



int part1(TYPE& inp, int y) {
    std::set<long long int> pos;
    std::set<long long int> bs;

    for (Sensor_Beacon& sb : inp) {
        if (sb.sensor.y == y) {
            bs.insert(pair(sb.sensor));
        }
        if (sb.beacon.y == y) {
            bs.insert(pair(sb.beacon));
        }
        int d = distance(sb.sensor, sb.beacon);
        if (sb.sensor.y + d >= y && sb.sensor.y - d <= y) {
            int m = std::abs(d-std::abs(sb.sensor.y - y));
            for (int i = -m; i <= m; i++) {
                Coordinate c = {
                    sb.sensor.x + i,
                    y
                };
                pos.insert(pair(c));
            }
        }
    }

    return pos.size() - bs.size();
}

long long int part2(TYPE& inp, int y) {
    int res = 0;

    std::map<int, std::vector<Range> > map;

    for (Sensor_Beacon& sb : inp) {
        int d = distance(sb.sensor, sb.beacon);
        for (int i = std::max(sb.sensor.x - d, 0); i <= std::min(sb.sensor.x + d, y); i++) {
            int d2 = d-std::abs(sb.sensor.x - i);
            Range r = {
                std::max(sb.sensor.y - d2, 0),
                std::min(sb.sensor.y + d2, y)
            };
            map[i].push_back(r);
        }
    }

    struct {
        bool operator()(Range r1, Range r2) const { return r1.min < r2.min; }
    } customLess;

    for (auto& i : map) {
        std::vector<Range> ranges = i.second;
        std::sort(ranges.begin(), ranges.end(), customLess);
        Range range = ranges[0];
        if (range.min > 0) {
            return i.first * 4000000;
        }
        for (int j = 0; j < ranges.size(); j++) {
            if (ranges[j].max >= 0) {
                range.max = ranges[j].max;
                break;
            }
        }
        for (Range r : ranges) {
            if (r.max > range.max) {
                if (r.min > range.max + 1) {
                    std::cout << "x=" << i.first << ", y=" << range.max + 1 << std::endl;
                    return i.first * 4000000 + range.max + 1;
                }
                range.max = r.max;
            }
        }
        if (range.max < y) {
            return i.first * 4000000 + y;
        }
    }

    return res;
}

int main() {
    TYPE test_inp = parse_input(YEAR "/tests/day_" DAY ".txt");
    TYPE inp = parse_input(YEAR "/inputs/day_" DAY ".txt");

    long long int expected_result_part1 = get_expected_result<long long int>(YEAR "/tests/results/day_" DAY "_1.txt");

    long long int res = part1(test_inp, 10);
    bool eval_res = evaluate_results(res, expected_result_part1);
    // res = part1(inp, 2000000);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    long long int expected_result_part2 = get_expected_result<long long int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp, 20);
    evaluate_results(res, expected_result_part2);
    res = part2(inp, 4000000);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
