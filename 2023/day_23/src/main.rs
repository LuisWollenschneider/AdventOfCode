use std::collections::{HashMap, HashSet};
use utils_rust::utils::wrapper;

const DAY: i32 = 23;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let (knots, start, end) = parse(input, true);

    longest_path(&knots, start, end).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (knots, start, end) = parse(input, false);

    longest_path(&knots, start, end).to_string()
}

fn longest_path(knots: &HashMap<(i64, i64), Vec<(i64, i64, i64)>>, start: (i64, i64), end: (i64, i64)) -> i64 {
    let mut dist_map: HashMap<(i64, i64), i64> = HashMap::new();

    let mut queue: Vec<(i64, i64, i64, HashSet<(i64, i64)>)> = Vec::new();
    let mut visited: HashSet<(i64, i64)> = HashSet::new();
    visited.insert(start);

    for (x, y, d) in knots.get(&start).unwrap() {
        queue.push((*x, *y, *d, visited.clone()));
    }

    while !queue.is_empty() {
        let (x, y, dist, visited) = queue.pop().unwrap();

        if visited.contains(&(x, y)) {
            continue;
        }

        let mut visited = visited.clone();
        visited.insert((x, y));

        if !dist_map.contains_key(&(x, y)) {
            dist_map.insert((x, y), dist);
        } else if dist_map.get(&(x, y)).unwrap() < &dist {
            dist_map.insert((x, y), dist);
        }

        for (nx, ny, d) in knots.get(&(x, y)).unwrap() {
            if visited.contains(&(*nx, *ny)) {
                continue;
            }
            queue.push((*nx, *ny, dist + d, visited.clone()));
        }
    }

    *dist_map.get(&end).unwrap_or(&-1)
}

// knots (x, y) -> [(x_i, y_i, dist)], start, end
fn parse(input: &String, slippery: bool) -> (HashMap<(i64, i64), Vec<(i64, i64, i64)>>, (i64, i64), (i64, i64)) {
    let height: i64 = input.lines().count() as i64;
    let width: i64 = input.lines().next().unwrap().chars().count() as i64;

    let mut nodes: HashMap<(i64, i64), char> = HashMap::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                continue;
            }
            nodes.insert((x as i64, y as i64), c);
        }
    }

    let mut child_map: HashMap<(i64, i64), Vec<(i64, i64)>> = HashMap::new();
    for ((x, y), c) in nodes.iter() {
        let mut children: Vec<(i64, i64)> = Vec::new();

        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)].iter() {
            let (nx, ny) = (x + dx, y + dy);

            if !nodes.contains_key(&(nx, ny)) {
                continue;
            }

            if slippery {
                if *c == '<' && *dx == 1 {
                    continue;
                }
                if *c == '>' && *dx == -1 {
                    continue;
                }
                if *c == '^' && *dy == 1 {
                    continue;
                }
                if *c == 'v' && *dy == -1 {
                    continue;
                }
            }

            children.push((nx, ny));
        }

        child_map.insert((*x, *y), children);
    }

    let mut furthest: HashMap<(i64, i64), Vec<(i64, i64, i64)>> = HashMap::new();
    for ((x, y), _) in nodes.iter() {
        let reachable_knots: Vec<(i64, i64, i64)> = reachable_knots(&child_map, (*x, *y));

        furthest.insert((*x, *y), reachable_knots);
    }

    let mut reachable_knots: HashSet<(i64, i64)> = HashSet::new();
    reachable_knots.insert((1, 0));

    loop {
        let mut new_reachable_knots: HashSet<(i64, i64)> = HashSet::new();
        for (x, y) in reachable_knots.iter() {
            new_reachable_knots.insert((*x, *y));
            for (nx, ny, _) in furthest.get(&(*x, *y)).unwrap() {
                new_reachable_knots.insert((*nx, *ny));
            }
        }
        if new_reachable_knots.len() == reachable_knots.len() {
            break;
        }
        reachable_knots = new_reachable_knots;
    }

    let knots: HashMap<(i64, i64), Vec<(i64, i64, i64)>> = furthest
        .iter()
        .filter(|((x, y), _)| reachable_knots.contains(&(*x, *y)))
        .map(|((x, y), v)| ((*x, *y), v.clone()))
        .collect();

    (knots, (1, 0), (width - 2, height - 1))
}


fn reachable_knots(child_map: &HashMap<(i64, i64), Vec<(i64, i64)>>, start: (i64, i64)) -> Vec<(i64, i64, i64)> {
    let mut res: Vec<(i64, i64, i64)> = Vec::new();

    let mut queue: Vec<(i64, i64, i64, HashSet<(i64, i64)>)> = Vec::new();
    let mut visited: HashSet<(i64, i64)> = HashSet::new();
    visited.insert(start);

    for (x, y) in child_map.get(&start).unwrap() {
        queue.push((*x, *y, 1, visited.clone()));
    }

    while !queue.is_empty() {
        let (x, y, dist, visited) = queue.pop().unwrap();

        if visited.contains(&(x, y)) {
            continue;
        }

        let mut visited = visited.clone();
        visited.insert((x, y));

        let children: Vec<(i64, i64)> = child_map.get(&(x, y)).unwrap()
            .iter()
            .filter(|(x, y)| !visited.contains(&(*x, *y)))
            .map(|(x, y)| (*x, *y))
            .collect();

        if children.len() == 1 {
            queue.push((children[0].0, children[0].1, dist + 1, visited.clone()));
        } else {
            res.push((x, y, dist));
        }
    }

    res
}