use std::iter::zip;
use utils_rust::utils::wrapper;

const DAY: i32 = 13;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    parse(input)
        .iter_mut()
        .map(|mirrors| mirrors.score())
        .sum::<u64>()
        .to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    parse(input)
        .iter_mut()
        .map(|mirrors| mirrors.new_score())
        .sum::<u64>()
        .to_string()
}

struct Mirrors {
    pattern: Vec<String>
}

impl Mirrors {
    fn score(&mut self) -> u64 {
        let h = self.horizontal();
        if h == 0 {
            self.vertical()
        } else {
            h * 100
        }
    }

    fn new_score(&mut self) -> u64 {
        let h = self.new_horizontal();
        if h == 0 {
            self.flip();
            self.new_vertical()
        } else {
            h * 100
        }
    }

    fn flip(&mut self) {
        let mut pattern: Vec<String> = Vec::new();
        for i in 0..self.pattern[0].len() {
            let mut line = String::new();
            for j in 0..self.pattern.len() {
                line.push(self.pattern[j].chars().nth(i).unwrap());
            }
            pattern.push(line);
        }
        self.pattern = pattern;
    }

    fn vertical(&mut self) -> u64 {
        self.flip();
        self.horizontal()
    }

    fn new_vertical(&self) -> u64 {
        self.new_horizontal()
    }

    fn horizontal(&self) -> u64 {
        for i in 1..self.pattern.len() {
            if self.pattern[..i].iter().rev().enumerate().all(
                |(j, l)| *l == *self.pattern.iter().nth(i + j).unwrap_or(l)
            ) {
                return i as u64
            }
        }
        0
    }

    fn new_horizontal(&self) -> u64 {
        for i in 1..self.pattern.len() {
            if self.pattern[..i].iter().rev().enumerate().map(
                |(j, l)| zip(l.chars(), self.pattern.iter().nth(i + j).unwrap_or(l).chars()).filter(
                    |(a, b)| *a != *b
                ).count()
            ).sum::<usize>() == 1 {
                return i as u64;
            }
        }
        0
    }
}

fn parse(input: &String) -> Vec<Mirrors> {
    input.split("\n\n")
        .map(|pattern| {
            let pattern: Vec<String> = pattern
                .split("\n")
                .map(|line| line.to_string())
                .collect::<Vec<String>>();
            Mirrors { pattern }
        })
        .collect()
}

fn abs(a: u64, b: u64) -> u64 {
    if a > b {
        a - b
    } else {
        b - a
    }
}