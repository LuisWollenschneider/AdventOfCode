use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 15;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    input.split(',').map(|s| hash(s.to_string())).sum::<u64>().to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let lenses = input
        .split(',')
        .map(|s| s.to_string())
        .map(|mut s| {
            if s.contains('=') {
                let (s, l) = s.split_once('=').unwrap();
                (hash(s.to_string()), s.to_string(), l.parse::<i64>().unwrap())
            } else {
                s.remove(s.len() - 1);
                (hash(s.clone()), s, -1)
            }
        })
        .collect::<Vec<(u64, String, i64)>>();

    let mut boxes: HashMap<u64, Vec<(String, i64)>> = HashMap::new();

    for lens in lenses {
        if !boxes.contains_key(&lens.0) {
            boxes.insert(lens.0, Vec::new());
        }
        let b = boxes.get_mut(&lens.0).unwrap();
        if lens.2 == -1 {
            let idx = b.iter().position(|(s, _)| s == &lens.1).unwrap_or(b.len());
            if idx != b.len() {
                b.remove(idx);
            }
        } else {
            let idx = b.iter().position(|(s, _)| s == &lens.1).unwrap_or(b.len());
            if idx == b.len() {
                b.push((lens.1, lens.2));
            } else {
                b[idx].1 = lens.2;
            }
        }
    }

    boxes
        .iter()
        .map(|(b, v)| v.iter().enumerate().map(|(i, (_, l))| (b + 1) as i64 * (i + 1) as i64 * *l).sum::<i64>())
        .sum::<i64>()
        .to_string()
}


fn hash(s: String) -> u64 {
    let mut hash: u64 = 0;
    for c in s.chars() {
        hash = (hash + c as u64) * 17 % 256;
    }
    hash
}