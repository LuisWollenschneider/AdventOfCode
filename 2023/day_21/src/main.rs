use std::collections::{HashSet, VecDeque};
use utils_rust::utils::wrapper;

const DAY: i32 = 21;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let steps: i64;
    if input.lines().count() == 11 {
        steps = 6;  // test input
    } else {
        steps = 64;
    }

    let (map, start) = parse(input);

    distances(&map, start, steps).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (map, start) = parse(input);

    let width = input.lines().next().unwrap().len() as i64;
    let height = input.lines().count() as i64;

    assert_eq!(width, height);

    let size = width;

    if size == 11 {
        // ignore test input
        return "0".to_string();
    }

    let steps = 26501365;

    let grids = steps / size - 1;

    assert_eq!((grids + 1) * size + size / 2, steps);

    let odd_grids = (grids / 2 * 2 + 1).pow(2) as u64;
    let even_grids = ((grids + 1) / 2 * 2).pow(2) as u64;

    let mut reachable: u64 = distances(&map, start, size * 2 + 1) * odd_grids;
    reachable += distances(&map, start, size * 2) * even_grids;

    let top = distances(&map, (start.0, size - 1), size - 1);
    let right = distances(&map, (0, start.1), size - 1);
    let bottom = distances(&map, (start.0, 0), size - 1);
    let left = distances(&map, (size - 1, start.1), size - 1);
    reachable += top + right + bottom + left;

    let top_right_1 = distances(&map, (0, size - 1), size / 2 - 1);
    let top_left_1 = distances(&map, (size - 1, size - 1), size / 2 - 1);
    let bottom_right_1 = distances(&map, (0, 0), size / 2 - 1);
    let bottom_left_1 = distances(&map, (size - 1, 0), size / 2 - 1);
    reachable += (top_right_1 + top_left_1 + bottom_right_1 + bottom_left_1) * (grids + 1) as u64;

    let top_right_2 = distances(&map, (0, size - 1), size * 3 / 2 - 1);
    let top_left_2 = distances(&map, (size - 1, size - 1), size * 3 / 2 - 1);
    let bottom_right_2 = distances(&map, (0, 0), size * 3 / 2 - 1);
    let bottom_left_2 = distances(&map, (size - 1, 0), size * 3 / 2 - 1);
    reachable += (top_right_2 + top_left_2 + bottom_right_2 + bottom_left_2) * grids as u64;

    reachable.to_string()
}

fn get_neighbors(map: &HashSet<(i64, i64)>, pos: (i64, i64)) -> HashSet<(i64, i64)> {
    let mut neighbors: HashSet<(i64, i64)> = HashSet::new();

    let (x, y) = pos;

    if map.contains(&(x - 1, y)) {
        neighbors.insert((x - 1, y));
    }

    if map.contains(&(x + 1, y)) {
        neighbors.insert((x + 1, y));
    }

    if map.contains(&(x, y - 1)) {
        neighbors.insert((x, y - 1));
    }

    if map.contains(&(x, y + 1)) {
        neighbors.insert((x, y + 1));
    }

    neighbors
}

fn distances(map: &HashSet<(i64, i64)>, start: (i64, i64), steps: i64) -> u64 {
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    let mut seen: HashSet<(i64, i64)> = HashSet::new();

    seen.insert(start);
    queue.push_back((start.0, start.1, steps));
    let mut reachable: HashSet<(i64, i64)> = HashSet::new();

    while !queue.is_empty() {
        let (x, y, steps) = queue.pop_front().unwrap();
        if steps < 0 {
            continue;
        }

        if steps % 2 == 0 {
            reachable.insert((x, y));
        }

        for neighbor in get_neighbors(&map, (x, y)) {
            if !seen.contains(&neighbor) {
                seen.insert(neighbor);
                queue.push_back((neighbor.0, neighbor.1, steps - 1));
            }
        }
    }

    reachable.len() as u64
}

fn parse(input: &String) -> (HashSet<(i64, i64)>, (i64, i64)) {
    let mut map: HashSet<(i64, i64)> = HashSet::new();

    let mut start: (i64, i64) = (-1, -1);

    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let x = x as i64;
            let y = y as i64;
            if c == '.' {
                map.insert((x, y));
            } else if c == 'S' {
                map.insert((x, y));
                start = (x, y);
            }
        }
    }

    (map, start)
}