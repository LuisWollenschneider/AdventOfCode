//
// Created by Wollenschneider Luis on 04.12.22.
//
#include <iostream>
#include <fstream>
#include <list>
#include <set>
#include <vector>
#include <stack>
#include <map>
#include <array>

#define COLOR_RED     "\x1b[31m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"
#define COLOR_RESET   "\x1b[0m"
#define COLOR_WHITE   "\x1b[0m"


std::string get_expected_result(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << COLOR_RED "File not found" COLOR_RESET << std::endl;
        // read use input
        std::cout << COLOR_BLUE "Enter expected result: " COLOR_RESET;
        std::string expected_result;
        std::cin >> expected_result;
        // create file with expected result as content at path filepath
        std::ofstream f(filepath);
        f << expected_result;
        return expected_result;
    }
    std::string line;
    std::getline(file, line);
    file.close();
    return line;
}

template<class T>
T get_expected_result(const std::string& filepath) {
    std::string line = get_expected_result(filepath);
    if (typeid(T) == typeid(int)) {
        return std::stoi(line);
    } else if (typeid(T) == typeid(long)) {
        return std::stol(line);
    } else if (typeid(T) == typeid(long long) || typeid(T) == typeid(long long int)) {
        return std::stoll(line);
    }
    std::cout << "Type not yet supported!" << std::endl;
    exit(1);
}

template <typename T>
bool evaluate_results(T test_result, T expected_result) {
    std::cout << COLOR_MAGENTA "TEST: " COLOR_RESET;
    if (test_result == expected_result) {
        std::cout << COLOR_GREEN << "PASSED" << COLOR_RESET << std::endl;
        return true;
    } else {
        std::cout << COLOR_RED << "FAILED" << COLOR_RESET << std::endl;
        std::cout << COLOR_BLUE << "Expected: " << expected_result << COLOR_RESET << std::endl;
        std::cout << COLOR_RED << "Got: " << test_result << COLOR_RESET << std::endl;
        return false;
    }
}

template <typename T>
void tried_before(T res, std::set<T>& tried) {
    if (tried.find(res) != tried.end()) {
        std::cout << COLOR_RED << "Already tried: " << res << COLOR_RESET << std::endl;
    }
}
