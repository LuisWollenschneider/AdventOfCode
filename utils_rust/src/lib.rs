#[allow(dead_code)]
pub mod utils {
    use std::fs::File;
    use std::io::{BufRead, BufReader, Read, Write};
    use std::io;
    use regex::Regex;

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

        input.trim().to_string()
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

    fn result_prompt(file_path: &String, part: i32) -> () {
        println!("{}Enter expected result for part {}{}{}:{}", BLUE, PINK, part, BLUE, RESET);

        let mut inp = String::new();
        io::stdin().read_line(&mut inp).unwrap();

        let mut file = File::create(file_path).unwrap();
        file.write_all(inp.trim().as_bytes()).unwrap();
    }

    fn get_cookie() -> String {
        let file = File::open("../../aoc_cookie.json").unwrap();
        let reader = BufReader::new(file);
        let json: serde_json::Value = serde_json::from_reader(reader).unwrap();
        // get cookie with key: "aoc-session-cookie"

        json["aoc-session-cookie"].as_str().unwrap().to_string()
    }

    fn fetch_input(year: i32, day: i32) -> () {
        println!("{}Fetching input for day {}{}{}...{}", YELLOW, PINK, day, YELLOW, RESET);

        let file_path = format!("../inputs/day_{:02}.txt", day);
        let url = format!("https://adventofcode.com/{}/day/{}/input", year, day);

        let cookie = get_cookie();

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

    fn submit_answer(year: i32, day: i32, part: i32, answer: String) -> () {
        let url = format!("https://adventofcode.com/{}/day/{}/answer", year, day);

        let cookie = get_cookie();

        let mut headers = reqwest::header::HeaderMap::new();
        headers.insert(reqwest::header::COOKIE, format!("session={}", cookie).parse().unwrap());

        let client = reqwest::blocking::Client::new();
        let mut response = client
            .post(&url)
            .headers(headers)
            .form(&[("level", part.to_string()), ("answer", answer)])
            .send()
            .unwrap();

        let mut resp = String::new();
        response.read_to_string(&mut resp).unwrap();

        let re = Regex::new(r"article>(.*)</article").unwrap();
        let resp = re.captures(&resp).unwrap()[1].to_string();
        let re = Regex::new(r"<a href.*?</a>").unwrap();
        let resp = re.replace_all(&resp, "");
        let resp = resp.replace("<p>", "").replace("</p>", "");

        if resp.contains("That's the right answer") {
            println!("{}That's the right answer!{}", YELLOW, RESET);
        } else if resp.contains("That's not the right answer") {
            println!("{}That's not the right answer!{}", RED, RESET);
        } else if resp.contains("Did you already complete it?") {
            println!("{}Already submitted!{}", DARK_ORANGE, RESET);
        } else {
            println!("{}Unknown response:{}", RED, RESET);
            println!("{}", resp);
        }
    }

    fn format_time(duration: std::time::Duration) -> String {
        let mut res: String = "".to_string();
        let secs = duration.as_secs();
        let millis = duration.subsec_millis() % 1000;
        let micros = duration.subsec_micros() % 1000;
        let nanos = duration.subsec_nanos() % 1000;
        
        if secs > 0 {
            res.push_str(&format!("{}{}{}s ", PINK, secs, DARK_ORANGE));
        }
        if millis > 0 || (!res.is_empty() && (micros > 0 || nanos > 0)) {
            res.push_str(&format!("{}{}{}ms ", PINK, millis, DARK_ORANGE));
        }
        if micros > 0 || (!res.is_empty() && nanos > 0) {
            res.push_str(&format!("{}{}{}μs ", PINK, micros, DARK_ORANGE));
        }
        if nanos > 0 || !res.is_empty() {
            res.push_str(&format!("{}{}{}ns ", PINK, nanos, DARK_ORANGE));
        }
        res
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
            result_prompt(&test_result_file_path, part);
        }
        let expected_result = get_input(&test_result_file_path)
            .trim()
            .to_string();

        print!("{}Running tests for part {}{}{}...{} ", BLUE, PINK, part, BLUE, RESET);

        let start = std::time::Instant::now();
        let test_result = func(&test_input);
        let duration = start.elapsed();

        println!("{}Done!{}", LIGHT_GREEN, RESET);

        if test_result.trim().to_string().eq("") {
            println!("{}Not Implemented!{}", DARK_ORANGE, RESET);
            return;
        }

        println!("{}Duration: {}{}", DARK_ORANGE, format_time(duration), RESET);

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


        print!("{}Running part {}{}{}... {}", BLUE, PINK, part, BLUE, RESET);

        let start = std::time::Instant::now();
        let result = func(&input);
        let duration = start.elapsed();

        println!("{}Done!{}", LIGHT_GREEN, RESET);

        println!("{}Duration: {}{}", DARK_ORANGE, format_time(duration), RESET);

        println!("{}Submit answer {}{}{} for part {}{}{}? {}", BLUE, LIGHT_GREEN, result, BLUE, PINK, part, BLUE, RESET);

        let mut inp = String::new();
        io::stdin().read_line(&mut inp).unwrap();

        if inp.trim().to_lowercase().eq("y") {
            submit_answer(year, day, part, result);
        }
    }
}
