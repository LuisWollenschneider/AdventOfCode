use std::collections::{HashMap, VecDeque};
use utils_rust::utils::wrapper;

const DAY: i32 = 17;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let (heatmap, width, height): (HashMap<(i64, i64), i64>, i64, i64) = parse(input);

    min_path(&heatmap, width, height, 1, 3).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (heatmap, width, height): (HashMap<(i64, i64), i64>, i64, i64) = parse(input);

    min_path(&heatmap, width, height, 4, 10).to_string()
}

fn min_path(map: &HashMap<(i64, i64), i64>, width: i64, height: i64, min: i64, max: i64) -> i64 {
    let mut min_heat_map_horizontally: HashMap<(i64, i64), i64> = HashMap::new();
    let mut min_heat_map_vertically: HashMap<(i64, i64), i64> = HashMap::new();

    //                        x, y, hor/vert, heat loss
    let mut dqueue: VecDeque<(i64, i64, bool, i64)> = VecDeque::new();
    dqueue.push_back((0, 0, true, 0));
    dqueue.push_back((0, 0, false, 0));

    let mut min_heat: i64 = i64::MAX;

    while !dqueue.is_empty() {
        let (x, y, dir, hl) = dqueue.pop_front().unwrap();

        if x < 0 || x >= width || y < 0 || y >= height {
            continue;
        }

        let heat_loss: i64 = hl;

        if x == width - 1 && y == height - 1 && heat_loss < min_heat {
            min_heat = heat_loss;
            println!("Heat loss: {}, queue: {}", heat_loss, dqueue.len());
            continue;
        }

        if dir {
            if heat_loss >= *min_heat_map_horizontally.get(&(x, y)).unwrap_or(&i64::MAX) {
                continue;
            }
            min_heat_map_horizontally.insert((x, y), heat_loss);

            let mut heat_loss_left: i64 = heat_loss;
            let mut heat_loss_right: i64 = heat_loss;

            for i in 1..min {
                heat_loss_right += map.get(&(x + i, y)).unwrap_or(&0);
                heat_loss_left += map.get(&(x - i, y)).unwrap_or(&0);
            }
            for i in min..max + 1 {
                heat_loss_right += map.get(&(x + i, y)).unwrap_or(&0);
                dqueue.push_back((x + i, y, false, heat_loss_right));

                heat_loss_left += map.get(&(x - i, y)).unwrap_or(&0);
                dqueue.push_back((x - i, y, false, heat_loss_left));
            }
        } else {
            if heat_loss >= *min_heat_map_vertically.get(&(x, y)).unwrap_or(&i64::MAX) {
                continue;
            }
            min_heat_map_vertically.insert((x, y), heat_loss);

            let mut heat_loss_up: i64 = heat_loss;
            let mut heat_loss_down: i64 = heat_loss;

            for i in 1..min {
                heat_loss_down += map.get(&(x, y + i)).unwrap_or(&0);
                heat_loss_up += map.get(&(x, y - i)).unwrap_or(&0);
            }
            for i in min..max + 1 {
                heat_loss_down += map.get(&(x, y + i)).unwrap_or(&0);
                dqueue.push_back((x, y + i, true, heat_loss_down));

                heat_loss_up += map.get(&(x, y - i)).unwrap_or(&0);
                dqueue.push_back((x, y - i, true, heat_loss_up));
            }
        }
    }

    min_heat
}

fn parse(input: &String) -> (HashMap<(i64, i64), i64>, i64, i64) {
    let mut map: HashMap<(i64, i64), i64> = HashMap::new();
    
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            map.insert((x as i64, y as i64), c.to_digit(10).unwrap() as i64);
        }
    }
    
    let height: i64 = input.lines().count() as i64;
    let width: i64 = input.lines().next().unwrap().chars().count() as i64;

    (map, width, height)
}
