use utils_rust::utils::wrapper;

const DAY: i32 = 7;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

struct Hand {
    bid: u64,
    rank: u64,
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
            let mut rank: u64 = 0;

            // let mut freq: HashMap<u64, u64> = HashMap::new();
            let mut freq: u64 = 0;
            let _ = cards.chars()
                .map(|c| {
                    let n = match c {
                        'T' => 10,
                        'J' => j,
                        'Q' => 12,
                        'K' => 13,
                        'A' => 14,
                        _ => c.to_string().parse::<u64>().unwrap()
                    };
                    freq += 1 << (n - 1) * 3;
                    // freq.insert(n, freq.get(&n).unwrap_or(&0) + 1);
                    rank = rank << 4 | n;
                })
                .collect::<Vec<_>>();
            let bid = bid.parse::<u64>().unwrap();

            let jokers = freq & 0b111;

            let mut freq = (1 .. 14)
                .map(|i| (freq >> (i * 3)) & 0b111)
                .collect::<Vec<u64>>();

            freq.sort();
            freq.reverse();

            rank |= match (freq[0] + jokers, freq[1]) {
                (5, _) => 0x7_00000,
                (4, _) => 0x6_00000,
                (3, 2) => 0x5_00000,
                (3, _) => 0x4_00000,
                (2, 2) => 0x3_00000,
                (2, _) => 0x2_00000,
                _ => 0x1_00000,
            };

            Hand { bid, rank }
        })
        .collect::<Vec<Hand>>();

    hands.sort_by_cached_key(|hand| hand.rank);

    hands
        .iter()
        .enumerate()
        .map(|(i, hand)| {
            hand.bid * (i as u64 + 1)
        })
        .sum::<u64>()
        .to_string()
}
