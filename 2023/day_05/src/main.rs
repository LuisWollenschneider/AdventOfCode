use utils_rust::utils::wrapper;

const DAY: i32 = 5;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let (seeds, rules) = parse_input(input);

    let seeds = seeds.iter().map(|x| (*x, 1)).collect::<Vec<_>>();

    get_min_location(&seeds, &rules).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (seeds, rules) = parse_input(input);

    let mut seed_ranges: Vec<(u64, u64)> = Vec::new();
    for i in (0..seeds.len()).step_by(2) {
        seed_ranges.push((seeds[i], seeds[i + 1]));
    }

    get_min_location(&seed_ranges, &rules).to_string()
}

#[allow(unused_variables)]
#[allow(dead_code)]
fn get_min_location(seeds: &Vec<(u64, u64)>, rules: &Vec<Vec<Vec<u64>>>) -> u64 {
    let mut start: Vec<(u64, u64)> = seeds.clone();

    let mut end: Vec<(u64, u64)> = Vec::new();

    for rule_set in rules {
        while !start.is_empty() {
            let new_start = start.clone();
            let (t, new_start) = new_start.split_at(1);
            let (s, r) = t[0];

            start = new_start.to_vec();

            let mut rule_found = false;
            let mut next_min: u64 = u64::MAX;
            for rule in rule_set.iter() {
                let (dest, source, r_) = (rule[0], rule[1], rule[2]);
                if source > s {
                    next_min = std::cmp::min(next_min, source);
                }

                if !(source <= s && s < source + r_) {
                    continue;
                }

                let used_range = std::cmp::min(r, source + r_ - s);
                end.push((s - source + dest, used_range));
                if used_range < r {
                    start.push((s + used_range, r - used_range));
                }
                rule_found = true;
                break;
            }
            if !rule_found {
                if next_min == u64::MAX {
                    end.push((s, r));
                } else {
                    if next_min - s < r {
                        end.push((s, next_min - s));
                        start.push((next_min, r - (next_min - s)));
                    } else {
                        end.push((s, r));
                    }
                }
            }
        }


        start = end.clone();
        end = Vec::new();
    };

    std::iter::
        once(start.iter().map(|x| x.0).collect::<Vec<_>>())
        .chain(std::iter::once(end.iter().map(|x| x.0).collect::<Vec<_>>()))
        .flatten()
        .min()
        .unwrap()
}

fn parse_input(input: &String) -> (Vec<u64>, Vec<Vec<Vec<u64>>>) {
    let conversions = input.split("\n\n").collect::<Vec<&str>>();

    let seeds: Vec<_> = conversions[0]
        .split(":")
        .collect::<Vec<&str>>()[1]
        .trim()
        .split(" ")
        .map(|x| x.parse::<u64>().unwrap())
        .collect();

    let rules: Vec<_> = conversions[1..]
        .iter()
        .map(
            |x| x.split("\n")
                // remove first line
                .skip(1)
                .map(|y| y.split(" ").collect::<Vec<&str>>())
                .map(|y| y.iter()
                    .map(|z| z.parse::<u64>().unwrap())
                    .collect::<_>()
                )
                .collect::<Vec<_>>()

        )
        .collect();

    (seeds, rules)
}