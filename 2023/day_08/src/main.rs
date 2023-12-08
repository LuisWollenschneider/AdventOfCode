use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 8;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
#[allow(unreachable_code)]
fn part_1(input: &String) -> String {
    let (instructions, nodes) = parse_input(input);

    let mut current = convert_node("AAA");
    let end = convert_node("ZZZ");

    let mut steps = 0;

    while current != end {
        for inst in instructions.chars() {
            match inst {
                'R' => {
                    let (l, r) = nodes.get(&current).unwrap();
                    current = *r;
                },
                'L' => {
                    let (l, r) = nodes.get(&current).unwrap();
                    current = *l;
                },
                _ => panic!("Invalid instruction: {}", inst),
            }
        }
        steps += 1;
    }

    (steps * instructions.len()).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (instructions, nodes) = parse_input(input);

    let mut precomputed_instructions: HashMap<u32, u32> = HashMap::new();
    for node in nodes.keys() {
        let mut end = *node;
        for inst in instructions.chars() {
            let (l, r) = nodes.get(&end).unwrap();
            match inst {
                'R' => {
                    if *r == 0 {
                        break;
                    }
                    end = *r;
                },
                'L' => {
                    if *l == 0 {
                        break;
                    }
                    end = *l;
                },
                _ => panic!("Invalid instruction: {}", inst),
            }
        }
        precomputed_instructions.insert(*node, end);
    }

    let min_steps_to_end: HashMap<u32, u32> = nodes
        .keys()
        .map(|node| {
            let mut steps = 0;
            let mut end = *node;
            while end & 0xff != 'Z' as u32 {
                let new_end = *precomputed_instructions.get(&end).unwrap();
                if new_end == end {
                    steps = u32::MAX;
                    break;
                }
                end = new_end;
                steps += 1;
            }
            (*node, steps)
        })
        .collect();

    let current_nodes: Vec<u32> = nodes
        .keys()
        .filter(|node|
            **node & 0xff == 'A' as u32
        )
        .map(|node| *node)
        .collect();

    (current_nodes
        .iter()
        .map(|node| std::cmp::max(*min_steps_to_end.get(&node).unwrap(), 1) as u64)
        .product::<u64>() * instructions.len() as u64).to_string()
}

fn convert_node(node: &str) -> u32 {
    node
        .chars()
        .enumerate()
        .map(|(i, c)| (c as u32) << ((2 - i) * 8))
        .sum::<u32>()
}

fn parse_input(input: &String) -> (String, HashMap<u32, (u32, u32)>) {
    let input = input
        .replace("(", "")
        .replace(")", "");
    let (instructions, nodes) = input
        .split_once("\n\n")
        .unwrap();

    let nodes: HashMap<u32, (u32, u32)> = nodes
        .lines()
        .map(|node| {
            let (node, inst) = node.split_once(" = ").unwrap();
            let (l, r) = inst.split_once(", ").unwrap();

            (convert_node(node), (convert_node(l), convert_node(r)))
        })
        .collect();

    (instructions.to_string(), nodes)
}