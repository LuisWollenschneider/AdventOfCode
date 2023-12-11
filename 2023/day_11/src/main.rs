use std::collections::HashSet;
use utils_rust::utils::wrapper;

const DAY: i32 = 11;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    solve(input, 2)
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    solve(input, 1_000_000)
}

fn solve(input: &String, factor: u64) -> String {
    let mut empty_cols: HashSet<usize> = HashSet::new();
    let mut empty_rows: HashSet<usize> = HashSet::new();
    let mut galaxies: Vec<(usize, usize)> = Vec::new();
    for (i, line) in input.lines().enumerate() {
        if line.chars().filter(|c| *c != '.').count() == 0 {
            empty_rows.insert(i);
        }
        if input.lines()
            .map(|line| line.chars().nth(i).unwrap())
            .filter(|c| *c != '.')
            .count() == 0 {
            empty_cols.insert(i);
        }
        line.chars()
            .enumerate()
            .filter(|(_, c)| *c == '#')
            .for_each(|(j, _)| galaxies.push((i, j)));
    }

    let mut res: u64 = 0;
    for (i, (x1, y1)) in galaxies.iter().enumerate() {
        for (x2, y2) in galaxies[i + 1..].iter() {
            res += manhattan_distance(*x1 as i32, *y1 as i32, *x2 as i32, *y2 as i32);
            let ys = if *y1 < *y2 { (*y1, *y2) } else { (*y2, *y1) };
            res += empty_rows.iter().filter(|x| **x > *x1 && **x < *x2).count() as u64 * (factor - 1);
            res += empty_cols.iter().filter(|y| **y > ys.0 && **y < ys.1).count() as u64 * (factor - 1);
        }
    }

    res.to_string()
}

fn manhattan_distance(x1: i32, y1: i32, x2: i32, y2: i32) -> u64 {
    ((x1 - x2).abs() + (y1 - y2).abs()) as u64
}