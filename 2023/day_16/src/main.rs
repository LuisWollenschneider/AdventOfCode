use std::collections::HashSet;
use utils_rust::utils::wrapper;

const DAY: i32 = 16;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let grid = parse(input);

    follow_beam(&grid, 0, 0, 1, 0).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let grid = parse(input);

    let height = grid.len();
    let width = grid[0].len();

    let mut res = 0;
    for y in 0..height {
        res = res.max(follow_beam(&grid, 0, y as i32, 1, 0));
        res = res.max(follow_beam(&grid, width as i32 - 1, y as i32, -1, 0));
    }

    for x in 0..width {
        res = res.max(follow_beam(&grid, x as i32, 0, 0, 1));
        res = res.max(follow_beam(&grid, x as i32, height as i32 - 1, 0, -1));
    }

    res.to_string()
}

fn follow_beam(grid: &Vec<Vec<char>>, x: i32, y: i32, dx: i32, dy: i32) -> u32 {
    let mut beams: HashSet<(i32, i32, i32, i32)> = HashSet::new();
    let mut visited: HashSet<(i32, i32, i32, i32)> = HashSet::new();
    let mut energized: HashSet<(i32, i32)> = HashSet::new();

    beams.insert((x, y, dx, dy));

    while !beams.is_empty() {
        let (bx, by, bdx, bdy) = beams.iter().next().unwrap().clone();
        beams.remove(&(bx, by, bdx, bdy));

        if bx < 0 || by < 0 || bx >= grid.len() as i32 || by >= grid[0].len() as i32 {
            continue;
        }

        if visited.contains(&(bx, by, bdx, bdy)) {
            continue;
        }
        visited.insert((bx, by, bdx, bdy));
        energized.insert((bx, by));

        let new_beams: Vec<(i32, i32, i32, i32)> = match grid[by as usize][bx as usize] {
            '.' => vec![(bx + bdx, by + bdy, bdx, bdy)],
            '/' => vec![(bx - bdy, by - bdx, -bdy, -bdx)],
            '\\' => vec![(bx + bdy, by + bdx, bdy, bdx)],
            '-' => {
                if bdx == 0 {
                    vec![(bx + bdy, by, bdy, 0), (bx - bdy, by, -bdy, 0)]
                } else {
                    vec![(bx + bdx, by + bdy, bdx, bdy)]
                }
            },
            '|' => {
                if bdy == 0 {
                    vec![(bx, by + bdx, 0, bdx), (bx, by - bdx, 0, -bdx)]
                } else {
                    vec![(bx + bdx, by + bdy, bdx, bdy)]
                }
            },
            _ => panic!("Invalid beam"),
        };

        beams.extend(new_beams);
    }

    energized.len() as u32
}

fn parse(input: &String) -> Vec<Vec<char>> {
    input
        .split("\n")
        .map(|x| x.chars().collect())
        .collect()
}