//
// Created by Wollenschneider Luis on 03.12.22.
//

#include "../utils.hpp"

#define DAY "12"
#define YEAR "2022"

struct Grid {
    std::vector<std::string> heights;
    std::vector<std::vector<int> > steps;
};

struct Coordinate {
    int x;
    int y;
};

#define TYPE Grid

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
        input.heights.push_back(line);
        input.steps.push_back(std::vector<int>());
        for (int i = 0; i < line.size(); i++) {
            input.steps.back().push_back(INT_MAX);
        }
    }
    file.close();
    return input;
}

Coordinate search_for(TYPE& input, char x, char r) {
    for (int i = 0; i < input.heights.size(); i++) {
        for (int j = 0; j < input.heights[i].size(); j++) {
            if (input.heights[i][j] == x) {
                input.heights[i][j] = r;
                Coordinate c = {i, j};
                return c;
            }
        }
    }
    Coordinate c = {-1, -1};
    return c;
}

Coordinate get_start(TYPE& input) {
    return search_for(input, 'S', 'a');
}

Coordinate get_end(TYPE& input) {
    return search_for(input, 'E', 'z');
}

std::vector<Coordinate> get_neighbours(const TYPE& inp, Coordinate s) {
    std::vector<Coordinate> v;
    if (s.x - 1 >= 0) {
        Coordinate c = {
                s.x - 1,
                s.y
        };
        v.push_back(c);
    }
    if (s.x + 1 < inp.heights.size()) {
        Coordinate c = {
                s.x + 1,
                s.y
        };
        v.push_back(c);
    }
    if (s.y - 1 >= 0) {
        Coordinate c = {
                s.x,
                s.y - 1
        };
        v.push_back(c);
    }
    if (s.y + 1 < inp.heights[0].size()) {
        Coordinate c = {
                s.x,
                s.y + 1
        };
        v.push_back(c);
    }
    return v;
}

void traverse_grid(TYPE& inp, const std::list<Coordinate>& s) {
    // BFS with previous visited nodes
    std::list<Coordinate> stack = s;
    while (!stack.empty()) {
        Coordinate c = stack.front();
        stack.pop_front();
        int steps = inp.steps[c.x][c.y];
        char height = inp.heights[c.x][c.y];

        std::vector<Coordinate> ns = get_neighbours(inp, c);

        for (Coordinate& n : ns) {
            // height difference?
            if (inp.heights[n.x][n.y] > height + 1) {
                continue;
            }
            // exists better way?
            if (inp.steps[n.x][n.y] <= steps) {
                continue;
            }
            inp.steps[n.x][n.y] = steps + 1;
            // only add to stack, if not already in line to be visited
            for (Coordinate& s2 : stack) {
                if (s2.x == n.x && s2.y == n.y) {
                    goto next;
                }
            }
            stack.push_back(n);
            next:;
        }
    }
}


int part1(TYPE& inp) {
    Coordinate s = get_start(inp);
    Coordinate e = get_end(inp);
    inp.steps[s.x][s.y] = 0;
    std::list<Coordinate> stack;
    stack.push_back(s);
    traverse_grid(inp, stack);

    return inp.steps[e.x][e.y];
}

std::list<Coordinate> get_starting_points(TYPE& inp) {
    std::list<Coordinate> l;
    for (int i = 0; i < inp.heights.size(); i++) {
        for (int j = 0; j < inp.heights[i].size(); j++) {
            if (inp.heights[i][j] == 'a' || inp.heights[i][j] == 'S') {
                inp.heights[i][j] = 'a';
                inp.steps[i][j] = 0;
                Coordinate c = {i, j};
                l.push_back(c);
            }
        }
    }
    return l;
}

int part2(TYPE& inp) {
    std::list<Coordinate> stack = get_starting_points(inp);
    Coordinate e = get_end(inp);
    traverse_grid(inp, stack);

    return inp.steps[e.x][e.y];
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
