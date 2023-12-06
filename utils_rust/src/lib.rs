#[allow(dead_code)]
pub mod utils {
    use std::fs::File;
    use std::io::{BufRead, BufReader, Read, Write};

    const BLUE: &str = "\x1b[94m";
    const RED: &str = "\x1b[91m";
    const GREEN: &str = "\x1b[32m";
    const LIGHT_GREEN: &str = "\x1b[92m";
    const YELLOW: &str = "\x1b[93m";
    const ORANGE: &str = "\x1b[31;1m";
    const PINK: &str = "\x1b[95m";
    const DARK_ORANGE: &str = "\x1b[33m";
    const RESET: &str = "\x1b[0m";

    fn get_input(file_path: &String) -> String {
        let file = File::open(file_path).unwrap();
        let reader = BufReader::new(file);

        let mut input: String = String::new();

        for line in reader.lines() {
            input.push_str(&line.unwrap());
            input.push('\n');
        }

        input
    }

    fn check_if_file_exists(file_path: &String) -> bool {
        match File::open(file_path) {
            Ok(_) => true,
            Err(_) => {
                eprintln!("File '{}' not found!", file_path);
                false
            },
        }
    }

    fn fetch_input(year: i32, day: i32) -> () {
        println!("{}Fetching input for day {}{}{}...", YELLOW, PINK, day, RESET);

        let file_path = format!("../inputs/day_{:02}.txt", day);
        let url = format!("https://adventofcode.com/{}/day/{}/input", year, day);

        // read json file with cookie
        let file = File::open("../../aoc_cookie.json").unwrap();
        let reader = BufReader::new(file);
        let json: serde_json::Value = serde_json::from_reader(reader).unwrap();
        // get cookie with key: "aoc-session-cookie"

        let cookie = json["aoc-session-cookie"].as_str().unwrap();

        let mut headers = reqwest::header::HeaderMap::new();
        headers.insert(reqwest::header::COOKIE, format!("session={}", cookie).parse().unwrap());

        let client = reqwest::blocking::Client::new();
        let mut response = client
            .get(&url)
            .headers(headers)
            .send()
            .unwrap();

        let mut input = String::new();
        response.read_to_string(&mut input).unwrap();

        let mut file = File::create(&file_path).unwrap();
        file.write_all(input.as_bytes()).unwrap();
    }

    pub fn wrapper(func: fn(&String) -> String, year: i32, day: i32, part: i32) {
        // check if test file exists
        let test_file_path = format!("../tests/day_{:02}.txt", day);
        if !check_if_file_exists(&test_file_path) {
            std::process::exit(1);
        }
        let test_input = get_input(&test_file_path);

        // check if test result file exists
        let test_result_file_path = format!("../tests/results/day_{:02}_{}.txt", day, part);
        if !check_if_file_exists(&test_result_file_path) {
            std::process::exit(1);
        }
        let expected_result = get_input(&test_result_file_path)
            .trim()
            .to_string();

        let test_result = func(&test_input);

        if test_result == expected_result {
            println!("\t{}TEST PASSED!{}", LIGHT_GREEN, RESET);
        } else {
            println!("\t{}TEST FAILED!", RED);
            println!("\t\tExpected: {}", expected_result);
            println!("\t\tGot:      {}{}", test_result, RESET);
            std::process::exit(1);
        }

        // check if input file exists
        let input_file_path = format!("../inputs/day_{:02}.txt", day);
        if !check_if_file_exists(&input_file_path) {
            fetch_input(year, day);
        }
        let input = get_input(&input_file_path);

        let result = func(&input);
        println!("{}Result - Part {}{}{}: {}{}{}", BLUE, PINK, part, BLUE, LIGHT_GREEN, result, RESET);
    }
}
