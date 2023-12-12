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
    records: String,
    groups: Vec<u64>
}

impl Springs {
    fn expand(&mut self) -> &mut Springs {
        let records = self.records.clone();
        let groups = self.groups.clone();
        for _ in 1..5 {
            self.records.push('?');
            self.records += &records;
            self.groups.extend(groups.clone());
        }
        self.total_springs *= 5;

        self
    }

    fn combinations(&self) -> u64 {
        let records = self.records.clone();
        let remaining_groups = self.groups.clone();


        let mut map: HashMap<String, u64> = HashMap::new();
        map.insert(records, 1);

        self.combinations_rec(map, &remaining_groups)
    }

    fn combinations_rec(&self,
                         mut map: HashMap<String, u64>,
                         remaining_groups: &Vec<u64>) -> u64 {
        if remaining_groups.len() == 0 {
            // all groups are placed
            return map
                .iter()
                .filter(|(k, _)| k.chars().all(|c| c != '#'))
                .map(|(_, v)| v)
                .sum::<u64>()
        }

        let group: u64 = remaining_groups[0];
        let remaining_groups: Vec<u64> = remaining_groups[1..].to_vec();

        let mut grouped_map: HashMap<String, u64> = HashMap::new();
        for (key, value) in map.iter_mut() {
            let mut rkey = key.clone();
            while !rkey.is_empty() {
                if rkey.starts_with('.') {
                    rkey.remove(0);
                    continue
                }

                let first_dot = rkey.find('.').unwrap_or(rkey.len());
                if first_dot < group as usize {
                    if first_dot == rkey.len() {
                        break
                    }

                    if rkey[..first_dot + 1].chars().any(|c| c == '#') {
                        break
                    }

                    rkey = rkey[first_dot + 1..].to_string();
                    continue
                }

                let mut new_key = "".to_string();
                let next_char = rkey.chars().nth(group as usize).unwrap_or('.');
                if group + 1 < rkey.len() as u64 {
                    new_key += &rkey[group as usize + 1..];
                }

                if next_char == '#' {
                    if rkey.starts_with('#') {
                        break
                    }
                    rkey.remove(0);
                    continue
                }

                if grouped_map.contains_key(&new_key) {
                    grouped_map.insert(new_key.clone(), grouped_map[&new_key] + *value);
                } else {
                    grouped_map.insert(new_key, *value);
                }

                if rkey.starts_with('#') {
                    break
                }
                rkey.remove(0);
            }
        }

        self.combinations_rec(grouped_map, &remaining_groups)
    }
}

fn parse(input: &String) -> Vec<Springs> {
    input
        .lines()
        .map(|line| {
            let (records, groups) = line.split_once(' ').unwrap();
            let groups: Vec<u64> = groups
                .split(",")
                .map(|group| group.parse::<u64>().unwrap())
                .collect();
            let records: String = records.to_string();
            Springs { records, groups }
        })
        .collect()
}