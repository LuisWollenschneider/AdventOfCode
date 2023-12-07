use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 7;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

struct Hand {
    cards: Vec<u64>,
    bid: u64,
    rank: u64,
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let mut hands: Vec<Hand> = parse_input(input, &"11".to_string());

    for hand in &mut hands {
        let mut dict: HashMap<u64, u64> = HashMap::new();
        for card in hand.cards.iter() {
            dict.insert(*card, dict.get(card).unwrap_or(&0) + 1);
        }
        // get values from dict, not keys
        let mut freq = dict.values()
            .map(|v| *v)
            .collect::<Vec<u64>>();
        freq.sort();
        freq.reverse();

        if freq[0] == 5 { // 5 of a kind
            hand.rank = 7;
        } else if freq[0] == 4 { // 4 of a kind
            hand.rank = 6;
        } else if freq[0] == 3 && freq[1] == 2 { // full house
            hand.rank = 5;
        } else if freq[0] == 3 { // 3 of a kind
            hand.rank = 4;
        } else if freq[0] == 2 && freq[1] == 2 { // 2 pairs
            hand.rank = 3;
        } else if freq[0] == 2 { // 1 pair
            hand.rank = 2;
        } else { // high card
            hand.rank = 1;
        }
    }

    get_result(hands)
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let mut hands: Vec<Hand> = parse_input(input, &"1".to_string());
    for hand in &mut hands {
        let mut dict: HashMap<u64, u64> = HashMap::new();
        let jokers: u64 = hand.cards.iter().filter(|c| **c == 1).count() as u64;
        for card in hand.cards.iter() {
            if *card != 1 {
                dict.insert(*card, dict.get(card).unwrap_or(&0) + 1);
            }
        }

        // get values from dict, not keys
        let mut freq = dict.values()
            .map(|v| *v)
            .collect::<Vec<u64>>();
        freq.push(0);
        freq.push(0);
        freq.sort();
        freq.reverse();

        if freq[0] + jokers == 5 { // 5 of a kind
            hand.rank = 7;
        } else if freq[0] + jokers == 4 { // 4 of a kind
            hand.rank = 6;
        } else if freq[0] + jokers == 3 && freq[1] == 2 { // full house
            hand.rank = 5;
        } else if freq[0] + jokers == 3 { // 3 of a kind
            hand.rank = 4;
        } else if freq[0] == 2 && freq[1] == 2 { // 2 pairs
            hand.rank = 3;
        } else if freq[0] + jokers == 2 { // 1 pair
            hand.rank = 2;
        } else { // high card
            hand.rank = 1;
        }
    }

    get_result(hands)
}

fn parse_input(input: &String, j: &String) -> Vec<Hand> {
    input
        .lines()
        .map(|line| line.to_string())
        .map(|line| line.split(" ")
            .map(|s| s.to_string())
            .collect::<Vec<String>>())
        // convert index 1 to u64 and keep index 0
        .map(|line| (
            // iterate over string
            line[0].chars()
                .map(|c| if c == 'T' { "10".to_string() }
                else if c == 'J' { j.to_string() }
                else if c == 'Q' { "12".to_string() }
                else if c == 'K' { "13".to_string() }
                else if c == 'A' { "14".to_string() }
                else { c.to_string() })
                .map(|s| s.parse::<u64>().unwrap())
                .collect::<Vec<u64>>(),
            line[1].parse::<u64>().unwrap())
        )
        .map(|(cards, bid)| Hand { cards, bid, rank: 0 })
        .collect::<Vec<Hand>>()
}

fn get_result(mut hands: Vec<Hand>) -> String {
    hands.sort_by(|a, b| {
        if a.rank == b.rank {
            for i in 0..a.cards.len() {
                if a.cards[i] != b.cards[i] {
                    return a.cards[i].cmp(&b.cards[i]);
                }
            }
            return a.cards[0].cmp(&b.cards[0]);
        }
        a.rank.cmp(&b.rank)
    });

    let mut res: u64 = 0;
    for i in 0..hands.len() {
        res += hands[i].bid * (i as u64 + 1);
    }

    res.to_string()
}