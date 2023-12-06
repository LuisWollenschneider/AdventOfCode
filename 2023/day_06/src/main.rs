use utils_rust::utils::wrapper;

const DAY: i32 = 6;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, DAY, 1);
    wrapper(part_2, DAY, 2);
}

fn part_1(input: &String) -> String {
    let mut result: u64 = 1;

    let input = input
        .lines()
        .map(|line| line.to_string())
        .collect::<Vec<String>>();

    let input: Vec<_> = input
        .iter()
        // Split lines at ": " and use the second part
        .map(|line| line.split(": ").collect::<Vec<&str>>()[1].to_string())
        // strip all spaces from start and end of each line
        .map(|line| line.trim().to_string())
        // split each line at spaces
        .map(|line| line.split(" ").map(|s| s.to_string()).collect::<Vec<String>>())
        // get rid of empty strings
        .map(|line| line.into_iter().filter(|s| s != "").collect::<Vec<String>>())
        .collect();

    let line1: Vec<_> = input[0].iter().collect();
    let line2: Vec<_> = input[1].iter().collect();

    for i in 0..line1.len() {
        let mut s = 0;
        let ms: u64 = line1[i].parse().unwrap();
        let max_dist: u64 = line2[i].parse().unwrap();
        for j in 1..(ms - 1) {
            if j * (ms - j) > max_dist {
                s += 1;
            }
        }
        result *= s;
    }

    result.to_string()
}

fn part_2(input: &String) -> String {
    let mut result: u64 = 0;

    let input = input
        .lines()
        .map(|line| line.to_string())
        .collect::<Vec<String>>();

    let input: Vec<_> = input
        .iter()
        // Split lines at ": " and use the second part
        .map(|line| line.split(": ").collect::<Vec<&str>>()[1].to_string())
        // remove all spaces
        .map(|line| line.replace(" ", ""))
        .collect();

    let ms: u64 = input[0].parse().unwrap();
    let max_dist: u64 = input[1].parse().unwrap();

    for j in 1..(ms - 1) {
        if j * (ms - j) > max_dist {
            result += 1;
        }
    }

    result.to_string()
}
