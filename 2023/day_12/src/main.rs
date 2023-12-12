use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 12;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    parse(input)
        .iter_mut()
        .map(|spring| spring.combinations())
        .sum::<u64>()
        .to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    parse(input)
        .iter_mut()
        .map(|spring| spring.expand().combinations())
        .sum::<u64>()
        .to_string()
}

struct Springs {
    records: Vec<char>,
    groups: Vec<usize>
}

impl Springs {
    fn expand(&mut self) -> &mut Springs {
        let records = self.records.clone();
        let groups = self.groups.clone();
        for _ in 1..5 {
            self.records.push('?');
            self.records.extend(records.clone());
            self.groups.extend(groups.clone());
        }
        self
    }

    fn combinations(&self) -> u64 {
        let mut map: HashMap<usize, u64> = HashMap::new();
        map.insert(0, 1);

        for group in self.groups.iter() {
            let mut grouped_map: HashMap<usize, u64> = HashMap::new();
            for (k, value) in map.iter() {
                let mut k = *k;
                while k + *group <= self.records.len() {
                    if self.records[k] == '.' {
                        k += 1;
                        continue
                    }

                    let next_dot = self.records[k..].iter().position(|c| *c == '.').unwrap_or(usize::MAX);
                    if next_dot < *group {
                        if next_dot == usize::MAX {
                            break
                        }

                        if self.records[k..k + next_dot + 1].iter().any(|c| *c == '#') {
                            break
                        }

                        k += next_dot + 1;
                        continue
                    }

                    let next_char = if *group + k < self.records.len() { self.records[*group + k] } else { '.' };
                    if next_char == '#' {
                        if self.records[k] == '#' {
                            break
                        }
                        k += 1;
                        continue
                    }

                    let mut new_key = self.records.len();
                    if k + *group + 1 < self.records.len() {
                        new_key = k + *group + 1 + self.records[k + *group + 1..].iter().position(|c| *c != '.').unwrap_or(0);
                    }

                    let entry = grouped_map.entry(new_key).or_insert(0);
                    *entry += value;

                    if self.records[k] == '#' {
                        break
                    }
                    k += 1;
                }
            }

            map = grouped_map;
        }

        let last = self.records.iter().rposition(|c| *c == '#').unwrap_or(0);

        map.iter()
            .filter(|(k, _)| **k > last)
            .map(|(_, v)| v)
            .sum::<u64>()
    }
}

fn parse(input: &String) -> Vec<Springs> {
    input
        .lines()
        .map(|line| {
            let (records, groups) = line.split_once(' ').unwrap();
            let groups: Vec<usize> = groups
                .split(",")
                .map(|group| group.parse::<usize>().unwrap())
                .collect();
            let records: Vec<char> = records.chars().collect();
            Springs { records, groups }
        })
        .collect()
}