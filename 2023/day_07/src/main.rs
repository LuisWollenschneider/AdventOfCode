use utils_rust::utils::wrapper;

const DAY: i32 = 7;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    solve(input, 11)
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    solve(input, 1)
}

fn solve(input: &String, j: u64) -> String {
    let mut hands = input
        .lines()
        .map(|line| {
            let (cards, bid) = line.split_once(" ").unwrap();

            // precalculate hand value
            // 0xR_12345, R: rank, 1-5: card values
            let mut rank: u64 = 0;

            // save frequency of each card as 3 bits
            // AKQ(J)T98765432(Joker)
            //    P1            P2
            let mut freq: u64 = 0;

            for c in cards.chars() {
                let n = match c {
                    'T' => 10,
                    'J' => j,
                    'Q' => 12,
                    'K' => 13,
                    'A' => 14,
                    _ => c as u64 - '0' as u64
                };
                freq += 1 << (n - 1) * 3;

                rank <<= 4;
                rank |= n;
            }
            let bid = bid.parse::<u64>().unwrap();

            // extract jokers
            let jokers = freq & 0b111;

            // 2 highest frequencies
            let mut m1 = 0;
            let mut m2 = 0;
            for _ in 1..14 {
                freq >>= 3;
                let f = freq & 0b111;
                if f == 0 {
                    continue;
                }
                if f > m1 {
                    m2 = m1;
                    m1 = f;
                } else if f > m2 {
                    m2 = f;
                }
            }

            // jokers = 0 for part 1
            // R value of hand value
            rank |= match (m1 + jokers, m2) {
                (5, _) => 0x7_00000,
                (4, _) => 0x6_00000,
                (3, 2) => 0x5_00000,
                (3, _) => 0x4_00000,
                (2, 2) => 0x3_00000,
                (2, _) => 0x2_00000,
                _ => 0x1_00000,
            };

            (bid, rank)
        })
        .collect::<Vec<(u64, u64)>>();

    // use cached sorting
    hands.sort_by_cached_key(|(_, rank)| *rank);

    // calculate total score
    hands
        .iter()
        .enumerate()
        .map(|(i, (bid, _))| {
            bid * (i as u64 + 1)
        })
        .sum::<u64>()
        .to_string()
}
