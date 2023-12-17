use std::cmp::Ordering;
use std::collections::{HashMap, BinaryHeap};
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

#[derive(Eq, PartialEq)]
struct Node {
    x: i64,
    y: i64,
    heat_loss: i64,
    dir: bool, // true = horizontal, false = vertical
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        self.heat_loss.cmp(&other.heat_loss)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(other.cmp(self))
    }
}

fn min_path(map: &HashMap<(i64, i64), i64>, width: i64, height: i64, min: i64, max: i64) -> i64 {
    let mut min_heat_map_horizontally: HashMap<(i64, i64), i64> = HashMap::new();
    let mut min_heat_map_vertically: HashMap<(i64, i64), i64> = HashMap::new();

    let mut pqueue: BinaryHeap<Node> = BinaryHeap::new();

    pqueue.push(Node { x: 0, y: 0, heat_loss: 0, dir: true });
    pqueue.push(Node { x: 0, y: 0, heat_loss: 0, dir: false });

    while !pqueue.is_empty() {
        let node: Node = pqueue.pop().unwrap();

        if node.x < 0 || node.x >= width || node.y < 0 || node.y >= height {
            continue;
        }

        if node.x == width - 1 && node.y == height - 1 {
            return node.heat_loss;
        }

        if node.dir {
            if node.heat_loss >= *min_heat_map_horizontally.get(&(node.x, node.y)).unwrap_or(&i64::MAX) {
                continue;
            }
            min_heat_map_horizontally.insert((node.x, node.y), node.heat_loss);

            let mut heat_loss_left: i64 = node.heat_loss;
            let mut heat_loss_right: i64 = node.heat_loss;

            for i in 1..min {
                heat_loss_right += map.get(&(node.x + i, node.y)).unwrap_or(&0);
                heat_loss_left += map.get(&(node.x - i, node.y)).unwrap_or(&0);
            }
            for i in min..max + 1 {
                heat_loss_right += map.get(&(node.x + i, node.y)).unwrap_or(&0);
                pqueue.push(Node { x: node.x + i, y: node.y, heat_loss: heat_loss_right, dir: false });

                heat_loss_left += map.get(&(node.x - i, node.y)).unwrap_or(&0);
                pqueue.push(Node { x: node.x - i, y: node.y, heat_loss: heat_loss_left, dir: false });
            }
        } else {
            if node.heat_loss >= *min_heat_map_vertically.get(&(node.x, node.y)).unwrap_or(&i64::MAX) {
                continue;
            }
            min_heat_map_vertically.insert((node.x, node.y), node.heat_loss);

            let mut heat_loss_up: i64 = node.heat_loss;
            let mut heat_loss_down: i64 = node.heat_loss;

            for i in 1..min {
                heat_loss_down += map.get(&(node.x, node.y + i)).unwrap_or(&0);
                heat_loss_up += map.get(&(node.x, node.y - i)).unwrap_or(&0);
            }
            for i in min..max + 1 {
                heat_loss_down += map.get(&(node.x, node.y + i)).unwrap_or(&0);
                pqueue.push(Node { x: node.x, y: node.y + i, heat_loss: heat_loss_down, dir: true });

                heat_loss_up += map.get(&(node.x, node.y - i)).unwrap_or(&0);
                pqueue.push(Node { x: node.x, y: node.y - i, heat_loss: heat_loss_up, dir: true });
            }
        }
    }

    -1
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
