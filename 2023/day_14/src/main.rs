use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 14;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let input = rotate_left(&input.split('\n').map(|s| s.to_string()).collect());

    let input = tilt_left(&input);
    calculate_weight(&input).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let mut input = rotate_left(&input.split('\n').map(|s| s.to_string()).collect());

    let mut cache: HashMap<Vec<String>, u64> = HashMap::new();
    let mut i: u64 = 0;
    while i < 1_000_000_000 {
        if cache.contains_key(&input) {
            let loop_size = i - cache.get(&input).unwrap();
            let loops = (1_000_000_000 - i) / loop_size;
            i += loops * loop_size;
        }

        cache.insert(input.clone(), i);
        i += 1;

        input = tilt_left(&input);  // tilt north
        input = rotate_right(&input);
        input = tilt_left(&input);  // tilt west
        input = rotate_right(&input);
        input = tilt_left(&input);  // tilt south
        input = rotate_right(&input);
        input = tilt_left(&input);  // tilt east
        input = rotate_right(&input);
    }

    calculate_weight(&input).to_string()
}

fn rotate_left(input: &Vec<String>) -> Vec<String> {
    let mut lines: Vec<String> = Vec::new();
    for i in 0..input[0].len() {
        let mut line = String::new();
        for j in 0..input.len() {
            line.push(input[j].chars().nth(i).unwrap());
        }
        lines.push(line);
    }
    lines
}

fn rotate_right(input: &Vec<String>) -> Vec<String> {
    let mut lines: Vec<String> = Vec::new();
    for i in (0..input[0].len()).rev() {
        let mut line = String::new();
        for j in 0..input.len() {
            line.push(input[j].chars().nth(i).unwrap());
        }
        lines.push(line);
    }
    lines
}

fn tilt_left(input: &Vec<String>) -> Vec<String> {
    let mut lines: Vec<String> = Vec::new();
    for line in input {
        let mut new_line = String::new();
        let mut last_empty = 0;
        for (i, c) in line.chars().enumerate() {
            match c {
                '#' => {
                    for _ in 0..i - last_empty {
                        new_line.push('.');
                    }
                    new_line.push('#');
                    last_empty = i + 1;
                }
                'O' => {
                    new_line.push('O');
                    last_empty += 1;
                }
                _ => {}
            }
        }
        for _ in 0..line.len() - last_empty {
            new_line.push('.');
        }
        lines.push(new_line);
    }
    lines
}

fn calculate_weight(input: &Vec<String>) -> u64 {
    let mut weight: u64 = 0;
    for line in input {
        for (i, c) in line.chars().enumerate() {
            if c == 'O' {
                weight += line.len() as u64 - i as u64;
            }
        }
    }
    weight
}