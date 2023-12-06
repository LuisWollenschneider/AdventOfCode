use std::fs::File;
use std::io::{BufRead, BufReader};

#[warn(unused_variables)]
fn main() {
    let file_path: &str = "../inputs/day_06.txt";
    let test_file_path: &str = "../tests/day_06.txt";

    let input = read_file(file_path);
    let test_input = read_file(test_file_path);

    // PART 1

    let expected_result: u64 = read_file("../tests/results/day_06_1.txt")[0]
        .parse()
        .unwrap();

    let test_result = part_1(&test_input);

    if test_result == expected_result {
        println!("Test successful!");
    } else {
        println!("Test failed!\n\tGot {}\n\tExpected {}", test_result, expected_result);
        std::process::exit(1);
    }

    let result = part_1(&input);
    println!("Result: {}", result);

    // PART 2

    let expected_result: u64 = read_file("../tests/results/day_06_2.txt")[0]
        .parse()
        .unwrap();

    let test_result = part_2(test_input);

    if test_result == expected_result {
        println!("Test successful!");
    } else {
        println!("Test failed!\n\tGot {}\n\tExpected {}", test_result, expected_result);
        std::process::exit(1);
    }

    let result = part_2(input);
    println!("Result: {}", result);
}

fn part_1(input: &Vec<String>) -> u64 {
    let mut result: u64 = 1;

    let input: Vec<_> = input
        .iter()
        // Split lines at ": " and use the second part
        .map(|line| line.split(": ").collect::<Vec<&str>>()[1].to_string())
        // strip all spaces from start and end of each line
        .map(|line| line.trim().to_string())
        // split each line at spaces
        .map(|line| line.split(" ").map(|s| s.to_string()).collect::<Vec<String>>())
        // get rid of empty strings
        .map(|line| line.into_iter().filter(|s| s != "").collect::<Vec<String>>())
        .collect();

    let line1: Vec<_> = input[0].iter().collect();
    let line2: Vec<_> = input[1].iter().collect();

    for i in 0..line1.len() {
        let mut s = 0;
        let ms: u64 = line1[i].parse().unwrap();
        let max_dist: u64 = line2[i].parse().unwrap();
        for j in 1..(ms - 1) {
            if j * (ms - j) > max_dist {
                s += 1;
            }
        }
        result *= s;
    }

    result
}

fn part_2(input: Vec<String>) -> u64 {
    let mut result: u64 = 0;

    let input: Vec<_> = input
        .iter()
        // Split lines at ": " and use the second part
        .map(|line| line.split(": ").collect::<Vec<&str>>()[1].to_string())
        // remove all spaces
        .map(|line| line.replace(" ", ""))
        .collect();

    let ms: u64 = input[0].parse().unwrap();
    let max_dist: u64 = input[1].parse().unwrap();

    for j in 1..(ms - 1) {
        if j * (ms - j) > max_dist {
            result += 1;
        }
    }

    result
}

fn read_file(file_path: &str) -> Vec<String> {
    let file = File::open(file_path).expect("File not found");
    let reader = BufReader::new(file);

    let mut input: Vec<String> = Vec::new();

    for line in reader.lines() {
        input.push(line.unwrap());
    }

    input
}
