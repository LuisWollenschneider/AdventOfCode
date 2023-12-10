use std::collections::HashSet;
use utils_rust::utils::wrapper;

const DAY: i32 = 10;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
#[allow(unreachable_code)]
fn part_1(input: &String) -> String {
    (get_circle_from_input(input).0.len() / 2).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (circle, circle_lines, width, height) = get_circle_from_input(input);
    count_enclosed_tiles(&circle, &circle_lines, width, height).to_string()
}

fn get_circle_from_input(input: &String) -> (Vec<(usize, usize)>, Vec<String>, usize, usize) {
    let lines: Vec<_> = input.split('\n')
        .map(|x| x.to_string())
        .collect();

    let width = lines[0].len();
    let height = lines.len();

    let (x, y) = locate_start(&lines);

    let mut circle: Vec<(usize, usize)> = Vec::new();
    let mut circle_lines: Vec<String> = Vec::new();

    let possible_chars = vec!['|', '-', 'L', 'J', '7', 'F'];
    let mut not_possible_chars: HashSet<char> = HashSet::new();
    if !check_north(x, y, &lines) {
        not_possible_chars.insert('|');
        not_possible_chars.insert('J');
        not_possible_chars.insert('L');
    }
    if !check_south(x, y, &lines, height) {
        not_possible_chars.insert('|');
        not_possible_chars.insert('7');
        not_possible_chars.insert('F');
    }
    if !check_east(x, y, &lines, width) {
        not_possible_chars.insert('-');
        not_possible_chars.insert('L');
        not_possible_chars.insert('F');
    }
    if !check_west(x, y, &lines) {
        not_possible_chars.insert('-');
        not_possible_chars.insert('7');
        not_possible_chars.insert('J');
    }

    for c in possible_chars.iter().filter(|x| !not_possible_chars.contains(x)) {
        circle_lines = input.replace('S', &*c.to_string())
            .split('\n')
            .map(|x| x.to_string())
            .collect::<Vec<_>>();

        let circ = get_circle(x, y, width, height, &circle_lines);
        if circ.is_none() {
            continue;
        }
        circle = circ.unwrap();
        break;
    }

    (circle, circle_lines, width, height)
}

fn locate_start(lines: &Vec<String>) -> (usize, usize) {
    for (y, line) in lines.iter().enumerate() {
        if line.contains('S') {
            return (line.find('S').unwrap(), y);
        }
    }

    panic!("No start found");
}

fn get_circle(mut x: usize,
              mut y: usize,
              width: usize,
              height: usize,
              lines: &Vec<String>) -> Option<Vec<(usize, usize)>> {
    let mut visited: Vec<(usize, usize)> = Vec::new();

    loop {
        visited.push((x, y));
        let coords = is_connected_twice(x, y, width, height, lines);
        if coords.is_none() {
            return None;
        }
        let ((x1, y1), (x2, y2)) = coords.unwrap();
        if !visited.contains(&(x1, y1)) {
            x = x1;
            y = y1;
        } else if !visited.contains(&(x2, y2)) {
            x = x2;
            y = y2;
        } else {
            return Some(visited);
        }
    }
}

fn is_connected_twice(x: usize,
                      y: usize,
                      width: usize,
                      height: usize,
                      lines: &Vec<String>) -> Option<((usize, usize), (usize, usize))> {
    match lines[y].chars().nth(x).unwrap() {
        '|' => {
            if check_north(x, y, lines) && check_south(x, y, lines, height) {
                Some(((x, y - 1), (x, y + 1)))
            } else {
                None
            }
        },
        '-' => {
            if check_west(x, y, lines) && check_east(x, y, lines, width) {
                Some(((x - 1, y), (x + 1, y)))
            } else {
                None
            }
        },
        'L' => {
            if check_north(x, y, lines) && check_east(x, y, lines, width) {
                Some(((x, y - 1), (x + 1, y)))
            } else {
                None
            }
        },
        'J' => {
            if check_north(x, y, lines) && check_west(x, y, lines) {
                Some(((x, y - 1), (x - 1, y)))
            } else {
                None
            }
        },
        '7' => {
            if check_south(x, y, lines, height) && check_west(x, y, lines) {
                Some(((x, y + 1), (x - 1, y)))
            } else {
                None
            }
        },
        'F' => {
            if check_south(x, y, lines, height) && check_east(x, y, lines, width) {
                Some(((x, y + 1), (x + 1, y)))
            } else {
                None
            }
        },
        _ => None
    }
}

fn check_north(x: usize, y: usize, lines: &Vec<String>) -> bool {
    if y == 0 {
        return false;
    }

    let north = lines[y - 1].chars().nth(x).unwrap();
    north == '|' || north == '7' || north == 'F'
}

fn check_south(x: usize, y: usize, lines: &Vec<String>, height: usize) -> bool {
    if y == height - 1 {
        return false;
    }

    let south = lines[y + 1].chars().nth(x).unwrap();
    south == '|' || south == 'L' || south == 'J'
}

fn check_west(x: usize, y: usize, lines: &Vec<String>) -> bool {
    if x == 0 {
        return false;
    }

    let west = lines[y].chars().nth(x - 1).unwrap();
    west == '-' || west == 'L' || west == 'F'
}

fn check_east(x: usize, y: usize, lines: &Vec<String>, width: usize) -> bool {
    if x == width - 1 {
        return false;
    }

    let east = lines[y].chars().nth(x + 1).unwrap();
    east == '-' || east == '7' || east == 'J'
}


fn count_enclosed_tiles(circle: &Vec<(usize, usize)>,
                        lines: &Vec<String>,
                        width: usize,
                        height: usize) -> i32 {
    let mut res = 0;
    let mut from = ' ';

    for y in 0..height {
        let mut c: i32 = 0;
        for x in 0..width {
            if circle.contains(&(x, y)) {
                c += match lines[y].chars().nth(x).unwrap() {
                    '|' => 1,
                    'F' => {from = 'F'; 0}
                    'L' => {from = 'L'; 0}
                    '7' => {if from == 'L' {1} else {0}}
                    'J' => {if from == 'F' {1} else {0}}
                    _ => 0
                };
            } else {
                res += c % 2;
            }
        }
    }

    res
}