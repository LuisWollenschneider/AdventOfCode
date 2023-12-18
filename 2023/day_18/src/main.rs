use utils_rust::utils::wrapper;

const DAY: i32 = 18;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let instructions = parse(input);
    let mut corners: Vec<(i64, i64)> = get_corners(&instructions);
    get_area(&mut corners).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let instructions: Vec<Instruction> = parse(input).iter_mut().map(|instruction| {
        instruction.direction = match instruction.color & 0xf {
            0 => 'R',
            1 => 'D',
            2 => 'L',
            3 => 'U',
            _ => panic!("Invalid color: {}", instruction.color)
        };
        instruction.distance = instruction.color >> 4;
        instruction.clone()
    })
    .collect();

    let mut corners: Vec<(i64, i64)> = get_corners(&instructions);
    get_area(&mut corners).to_string()
}

fn get_corners(instructions: &Vec<Instruction>) -> Vec<(i64, i64)> {
    let mut corners: Vec<(i64, i64)> = Vec::new();
    let mut last_corner: (i64, i64) = (0, 0);

    for instruction in instructions {
        let dir = convert_direction(instruction.direction);
        last_corner = (last_corner.0 + dir.0 * instruction.distance, last_corner.1 + dir.1 * instruction.distance);
        corners.push(last_corner);
    }

    corners
}

fn get_area(corners: &mut Vec<(i64, i64)>) -> i64 {
    corners.push(corners[0]);

    let mut area: i64 = 0;
    let mut edge_area: i64 = 0;
    for i in 0..corners.len() - 1 {
        area += corners[i].0 * corners[i + 1].1 - corners[i + 1].0 * corners[i].1;
        edge_area += (corners[i].0 - corners[i + 1].0).abs() + (corners[i].1 - corners[i + 1].1).abs();
    }

    area.abs() / 2 + edge_area / 2 + 1
}

fn convert_direction(direction: char) -> (i64, i64) {
    match direction {
        'U' => (0, -1),
        'D' => (0, 1),
        'L' => (-1, 0),
        'R' => (1, 0),
        _ => panic!("Invalid direction: {}", direction)
    }
}

#[derive(Clone)]
struct Instruction {
    direction: char,
    distance: i64,
    color: i64,
}

fn parse(input: &String) -> Vec<Instruction> {
    input
        .lines()
        .map(|line| {
            let split: Vec<&str> = line.split(' ').collect();
            Instruction {
                direction: split[0].chars().next().unwrap(),
                distance: split[1].parse::<i64>().unwrap(),
                color: i64::from_str_radix(split[2].replace("(#", "").replace(")", "").as_str(), 16).unwrap()
            }
        })
        .collect()
}