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
    let lines: Vec<_> = input.split('\n')
        .collect();

    let width = lines[0].len();
    let height = lines.len();

    let (x, y) = locate_start(&lines);

    let mut res = 0;

    for c in vec!['|', '-', 'L', 'J', '7', 'F'] {
        let _lines = lines
            .clone()
            .iter()
            .map(|x| x.replace('S', &*c.to_string()))
            .collect::<Vec<_>>();

        let circle = get_circle(x, y, &_lines);
        if circle.is_none() {
            continue;
        }
        res = std::cmp::max(circle.unwrap().len(), res);
    }

    (res / 2).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let lines: Vec<_> = input.split('\n')
        .collect();

    let width = lines[0].len();
    let height = lines.len();

    let (x, y) = locate_start(&lines);

    let mut circle: Vec<(usize, usize)> = Vec::new();
    let mut circle_lines: Vec<String> = Vec::new();

    for c in vec!['|', '-', 'L', 'J', '7', 'F'] {
        let _lines = lines
            .clone()
            .iter()
            .map(|x| x.replace('S', &*c.to_string()))
            .collect::<Vec<_>>();

        let circ = get_circle(x, y, &_lines);
        if circ.is_none() {
            continue;
        }
        let circ = circ.clone().unwrap();
        if circ.len() > circle.len() {
            circle = circ;
            circle_lines = _lines;
        }
    }

    count_enclosed_tiles(&circle, &circle_lines, width, height).to_string()
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
                c += match lines[y].chars().nth(x) {
                    Some('|') => 1,
                    Some('F') => {from = 'F'; 0}
                    Some('L') => {from = 'L'; 0}
                    Some('7') => {if from == 'L' {1} else {0}}
                    Some('J') => {if from == 'F' {1} else {0}}
                    _ => 0
                };
            } else {
                res += c % 2;
            }
        }
    }

    res
}

fn locate_start(lines: &Vec<&str>) -> (usize, usize) {
    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == 'S' {
                return (x, y);
            }
        }
    }

    panic!("No start found");
}

fn get_circle(mut x: usize, mut y: usize, lines: &Vec<String>) -> Option<Vec<(usize, usize)>> {
    let mut visited: Vec<(usize, usize)> = Vec::new();

    loop {
        visited.push((x, y));
        let coords = is_connected_twice(x, y, lines);
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

fn is_connected_twice(x: usize, y: usize, lines: &Vec<String>) -> Option<((usize, usize),
                                                                           (usize, usize))> {
    match lines[y].chars().nth(x) {
        Some('|') => {
            if check_north(x, y, lines) && check_south(x, y, lines) {
                Some(((x, y - 1), (x, y + 1)))
            } else {
                None
            }
        },
        Some('-') => {
            if check_west(x, y, lines) && check_east(x, y, lines) {
                Some(((x - 1, y), (x + 1, y)))
            } else {
                None
            }
        },
        Some('L') => {
            if check_north(x, y, lines) && check_east(x, y, lines) {
                Some(((x, y - 1), (x + 1, y)))
            } else {
                None
            }
        },
        Some('J') => {
            if check_north(x, y, lines) && check_west(x, y, lines) {
                Some(((x, y - 1), (x - 1, y)))
            } else {
                None
            }
        },
        Some('7') => {
            if check_south(x, y, lines) && check_west(x, y, lines) {
                Some(((x, y + 1), (x - 1, y)))
            } else {
                None
            }
        },
        Some('F') => {
            if check_south(x, y, lines) && check_east(x, y, lines) {
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

    let north = lines[y - 1].chars().nth(x);
    if north == Some('|') || north == Some('7') || north == Some('F') {
        return true;
    }

    false
}

fn check_south(x: usize, y: usize, lines: &Vec<String>) -> bool {
    if y == lines.len() - 1 {
        return false;
    }

    let south = lines[y + 1].chars().nth(x);
    if south == Some('|') || south == Some('J') || south == Some('L') {
        return true;
    }

    false
}

fn check_west(x: usize, y: usize, lines: &Vec<String>) -> bool {
    if x == 0 {
        return false;
    }

    let west = lines[y].chars().nth(x - 1);
    if west == Some('-') || west == Some('L') || west == Some('F') {
        return true;
    }

    false
}

fn check_east(x: usize, y: usize, lines: &Vec<String>) -> bool {
    if x == lines[y].len() - 1 {
        return false;
    }

    let east = lines[y].chars().nth(x + 1);
    if east == Some('-') || east == Some('J') || east == Some('7') {
        return true;
    }

    false
}