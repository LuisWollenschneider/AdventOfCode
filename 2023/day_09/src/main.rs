use utils_rust::utils::wrapper;

const DAY: i32 = 9;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    solve(input, 1)
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    solve(input, 0)
}

fn solve(input: &String, i: usize) -> String {
    input
        .lines()
        .map(|line| line.split(' ')
            .map(|num| num.parse::<i64>().unwrap())
            .collect()
        )
        .map(|sequence| get_next_number(&sequence)[i])
        .sum::<i64>().to_string()
}

fn get_next_number(sequence: &Vec<i64>) -> Vec<i64> {
    let diffs: Vec<i64> = sequence
        .iter()
        .take(sequence.len() - 1)
        .enumerate()
        .map(|(i, num)|
            sequence[i + 1] - num
        )
        .collect();

    if diffs.iter().any(|&diff| diff != 0) {
        let d = get_next_number(&diffs);
        vec!(sequence[0] - d[0], sequence[sequence.len() - 1] + d[1])
    } else {
        vec!(sequence[0], sequence[sequence.len() - 1])
    }
}