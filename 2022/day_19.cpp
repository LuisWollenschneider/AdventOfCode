//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "19"
#define YEAR "2022"
#define RETURN_TYPE int

struct Blueprint {
    int ore_ore;
    int clay_ore;
    int obsidian_ore;
    int obsidian_clay;
    int geode_ore;
    int geode_obsidian;
};

#define TYPE std::vector<Blueprint>

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
        // Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        Blueprint b = {
                .ore_ore = std::stoi(line.substr(line.find("Each ore robot costs ") + 21)),
                .clay_ore = std::stoi(line.substr(line.find("Each clay robot costs ") + 22)),
                .obsidian_ore = std::stoi(line.substr(line.find("Each obsidian robot costs ") + 26)),
                .obsidian_clay = std::stoi(line.substr(line.find("ore and ") + 8)),
                .geode_ore = std::stoi(line.substr(line.find("Each geode robot costs ") + 23)),
                .geode_obsidian = std::stoi(line.substr(line.find_last_of("ore and ") - 10)),
        };
        input.push_back(b);
    }
    file.close();
    return input;
}

int simulate_blueprint(const Blueprint &blueprint,
                       int ore_robots, int clay_robots, int obsidian_robots, int geode_robots,
                       int ore, int clay, int obsidian, int geode, int minutes,
                       std::set<long long int>* seen) {
    if (minutes == 0) {
        return geode;
    }

    int m = 0;
    // mine
    int max_req_ore = std::max(std::max(blueprint.ore_ore, blueprint.clay_ore), std::max(blueprint.obsidian_ore, blueprint.geode_ore));
    int new_ore = std::min(ore + ore_robots, minutes * max_req_ore);
    int new_clay = std::min(clay + clay_robots, minutes * blueprint.obsidian_clay);
    int new_obsidian = std::min(obsidian + obsidian_robots, minutes * blueprint.geode_obsidian);
    int new_geode = geode + geode_robots;

    minutes--;

    long long int s = ore_robots;
    s = s << 5 | clay_robots;
    s = s << 5 | obsidian_robots;
    s = s << 5 | geode_robots;
    s = s << 8 | new_ore;
    s = s << 10 | new_clay;
    s = s << 10 | new_obsidian;
    s = s << 10 | new_geode;
    s = s << 5 | minutes;

    if (seen->find(s) != seen->end()) {
        return 0;
    }
    seen->insert(s);

    int mm = INT_MAX; // minutes * (minutes + 1) / 2 + geode_robots * minutes;
    // std::cout << "minutes: " << minutes << " geode_robots: " << geode_robots << " mm: " << mm << std::endl;
    // exit(0);

    // try build geode robots
    if (ore >= blueprint.geode_ore && obsidian >= blueprint.geode_obsidian) {
        m = std::max(m, simulate_blueprint(blueprint, ore_robots, clay_robots, obsidian_robots, geode_robots + 1,
                                           new_ore - blueprint.geode_ore, new_clay,
                                           new_obsidian - blueprint.geode_obsidian, new_geode, minutes, seen));
    }
    // try build obsidian robots
    if (ore >= blueprint.obsidian_ore && clay >= blueprint.obsidian_clay) {
        if (obsidian_robots < blueprint.geode_obsidian) {
            if (mm > m) {
                m = std::max(m,
                             simulate_blueprint(blueprint, ore_robots, clay_robots, obsidian_robots + 1, geode_robots,
                                                new_ore - blueprint.obsidian_ore, new_clay - blueprint.obsidian_clay,
                                                new_obsidian, new_geode, minutes, seen));
            }
        }
    }
    // try build clay robots
    if (ore >= blueprint.clay_ore) {
        if (clay_robots < blueprint.obsidian_clay) {
            if (mm > m) {
                m = std::max(m,
                             simulate_blueprint(blueprint, ore_robots, clay_robots + 1, obsidian_robots, geode_robots,
                                                new_ore - blueprint.clay_ore, new_clay, new_obsidian, new_geode,
                                                minutes, seen));
            }
        }
    }
    // try build ore robots
    if (ore >= blueprint.ore_ore) {
        if (ore_robots < max_req_ore) {
            if (mm > m) {
                m = std::max(m,
                             simulate_blueprint(blueprint, ore_robots + 1, clay_robots, obsidian_robots, geode_robots,
                                                new_ore - blueprint.ore_ore, new_clay, new_obsidian, new_geode,
                                                minutes, seen));
            }
        }
    }
    // build no robots
    if (mm > m) {
        m = std::max(m, simulate_blueprint(blueprint, ore_robots, clay_robots, obsidian_robots, geode_robots,
                                           new_ore, new_clay, new_obsidian, new_geode, minutes, seen));
    }
    return m;
}

int start_simulation(Blueprint &b, int minutes) {
    std::set<long long int> seen = std::set<long long int>();
    return simulate_blueprint(b,
                              1, 0, 0, 0,
                              0, 0, 0, 0,
                              minutes, &seen);
}

int part1(TYPE &inp) {
    int res = 0;

    int i = 1;
    for (Blueprint &b : inp) {
        int s = start_simulation(b, 24);
        // std::cout << "Blueprint " << i << ": " << s << std::endl;
        res += i * s;
        i++;
    }

    return res;
}

int part2(TYPE &inp) {
    int res = 1;

    int i = 1;
    for (Blueprint &b : inp) {
        int s = start_simulation(b, 32);
        std::cout << "Blueprint " << i << ": " << s << std::endl;
        res *= s;
        i++;
        if (i > 3) {
            break;
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
    std::set<int> tried;
    tried.insert(1542);
    tried_before(res, tried);
    std::cout << "Part 1: " << res << std::endl;

    if (!eval_res) {
        return 1;
    }

    std::cout << std::endl;
    int expected_result_part2 = get_expected_result<int>(YEAR "/tests/results/day_" DAY "_2.txt");

    res = part2(test_inp);
    evaluate_results(res, expected_result_part2);
    res = part2(inp);
    std::set<int> tried2;
    tried_before(res, tried2);
    std::cout << "Part 2: " << res << std::endl;

    return 0;
}
