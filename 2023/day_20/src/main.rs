use std::collections::{HashMap, VecDeque};
use utils_rust::utils::wrapper;

const DAY: i32 = 20;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let mut modules: HashMap<String, Box<dyn Signal>> = parse(input);

    let mut lows: u64 = 0;
    let mut highs: u64 = 0;

    for i in 0..1000 {
        // caching possible, but only the sample input contains loops for cycles < 1000

        let mut queue: VecDeque<(String, String, bool)> = VecDeque::new();

        queue.push_back(("button".to_string(), "broadcaster".to_string(), false));

        while !queue.is_empty() {
            let (sender, receiver, signal) = queue.pop_front().unwrap();

            if signal {
                highs += 1;
            } else {
                lows += 1;
            }

            if !modules.contains_key(&receiver) {
                continue;
            }

            let mut new_signals: VecDeque<(String, bool)> = modules.get_mut(&receiver).unwrap().pulse(&sender, signal);

            while !new_signals.is_empty() {
                let (recv, signal) = new_signals.pop_front().unwrap();
                queue.push_back((receiver.clone(), recv, signal));
            }
        }
    }

    (lows * highs).to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let mut modules: HashMap<String, Box<dyn Signal>> = parse(input);

    if modules.len() < 10 {
        // dummy output for sample input, since sample input does not contain "rx"
        return "0".to_string();
    }

    let mut rx_parent: Vec<String> = Vec::new();
    for (name, module) in &modules {
        if module.dest().contains(&"rx".to_string()) {
            rx_parent.push(name.clone());
        }
    }

    let mut rx_parent_parents: Vec<String> = Vec::new();
    for parent in &rx_parent {
        for (name, module) in &modules {
            if module.dest().contains(parent) {
                rx_parent_parents.push(name.clone());
            }
        }
    }

    get_steps_till_high_pulse(
        &mut modules,
        rx_parent_parents
    ).iter()
        .map(|(name, steps)| *steps)
        .reduce(|a, b| lcm(a, b))
        .unwrap()
        .to_string()
}

fn lcm(a: u64, b: u64) -> u64 {
    a * b / gcd(a, b)
}

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 {
        return a;
    }
    gcd(b, a % b)
}

fn get_steps_till_high_pulse(modules: &mut HashMap<String, Box<dyn Signal>>,
                             mut module_of_interest: Vec<String>) -> HashMap<String, u64> {
    let mut found: HashMap<String, u64> = HashMap::new();
    let mut i: u64 = 0;

    loop {
        let mut queue: VecDeque<(String, String, bool)> = VecDeque::new();
        let mut module_highs: HashMap<String, u64> = HashMap::new();

        for module in &module_of_interest {
            module_highs.insert(module.clone(), 0);
        }

        queue.push_back(("button".to_string(), "broadcaster".to_string(), false));

        while !queue.is_empty() {
            let (sender, receiver, signal) = queue.pop_front().unwrap();

            for module in &module_of_interest {
                if signal && sender == module.as_str() {
                    module_highs.insert(module.clone(), module_highs.get(module).unwrap() + 1);
                }
            }

            if !modules.contains_key(&receiver) {
                continue;
            }

            let mut new_signals: VecDeque<(String, bool)> = modules.get_mut(&receiver).unwrap().pulse(&sender, signal);

            while !new_signals.is_empty() {
                let (recv, signal) = new_signals.pop_front().unwrap();
                queue.push_back((receiver.clone(), recv, signal));
            }
        }

        i += 1;

        for (module, highs) in &module_highs {
            if *highs == 1 {
                found.insert(module.clone(), i);
                module_of_interest.retain(|x| x != module);
            }
        }

        if module_of_interest.is_empty() {
            break;
        }
    }

    found
}

/*
 * Used for caching, but was removed later on
 */
#[allow(dead_code)]
fn get_state(modules: &HashMap<String, Box<dyn Signal>>) -> Vec<(String, u64)> {
    let mut state: Vec<(String, u64)> = Vec::new();

    let mut keys: Vec<String> = modules.keys().map(|x| x.clone()).collect();
    keys.sort();

    for key in keys {
        state.push((key.clone(), modules.get(key.as_str()).unwrap().state()));
    }

    state
}

trait Signal {
    fn pulse(&mut self, sender: &String, signal: bool) -> VecDeque<(String, bool)>;

    #[allow(unused_variables)]
    fn init(&mut self, sender: String) {}

    fn state(&self) -> u64;

    fn dest(&self) -> Vec<String>;
}

struct Module {
    dest: Vec<String>
}

impl Signal for Module {
    fn pulse(&mut self, _: &String, signal: bool) -> VecDeque<(String, bool)> {
        let mut out: VecDeque<(String, bool)> = VecDeque::new();

        for dest in &self.dest {
            out.push_back((dest.clone(), signal));
        }
        out
    }

    fn state(&self) -> u64 {
        0
    }

    fn dest(&self) -> Vec<String> {
        self.dest.clone()
    }
}

struct FlipFlop {
    state: bool,  // default false
    dest: Vec<String>
}

impl Signal for FlipFlop {
    fn pulse(&mut self, _: &String, signal: bool) -> VecDeque<(String, bool)> {
        if signal {
            return VecDeque::new();
        }
        let mut out: VecDeque<(String, bool)> = VecDeque::new();

        self.state = !self.state;

        for dest in &self.dest {
            out.push_back((dest.clone(), self.state));
        }
        out
    }

    fn state(&self) -> u64 {
        self.state as u64
    }

    fn dest(&self) -> Vec<String> {
        self.dest.clone()
    }
}

struct Conjunction {
    states: HashMap<String, bool>, // default false
    dest: Vec<String>
}

impl Signal for Conjunction {
    fn pulse(&mut self, sender: &String, signal: bool) -> VecDeque<(String, bool)> {
        self.states.insert(sender.clone(), signal);

        let sig: bool = !self.states.values().all(|&x| x);

        let mut out: VecDeque<(String, bool)> = VecDeque::new();

        for dest in &self.dest {
            out.push_back((dest.clone(), sig));
        }
        out
    }

    fn init(&mut self, sender: String) {
        self.states.insert(sender.clone(), false);
    }

    fn state(&self) -> u64 {
        let mut x: u64 = 0;
        for (_, &state) in &self.states {
            x = x << 1 | state as u64;
        }
        x
    }

    fn dest(&self) -> Vec<String> {
        self.dest.clone()
    }
}

fn parse(input: &String) -> HashMap<String, Box<dyn Signal>> {
    let mut modules: HashMap<String, Box<dyn Signal>> = HashMap::new();

    for line in input.lines() {
        let module: Box<dyn Signal>;
        let (mut name, dests) = line.split_once(" -> ").unwrap();
        if name.starts_with('%') {
            // FlipFlop
            name = name.trim_start_matches('%');
            let mut dest: Vec<String> = Vec::new();
            for d in dests.split(", ") {
                dest.push(d.to_string());
            }
            module = Box::new(FlipFlop { state: false, dest });
        } else if name.starts_with('&') {
            // Conjunction
            name = name.trim_start_matches('&');
            let mut dest: Vec<String> = Vec::new();
            for d in dests.split(", ") {
                dest.push(d.to_string());
            }
            module = Box::new(Conjunction { states: HashMap::new(), dest });
        } else {
            // Module
            let mut dest: Vec<String> = Vec::new();
            for d in dests.split(", ") {
                dest.push(d.to_string());
            }
            module = Box::new(Module { dest });
        }

        modules.insert(name.to_string(), module);
    }

    let keys: Vec<String> = modules.keys().map(|x| x.clone()).collect();
    for name in keys {
        for dest in modules.get(name.clone().as_str()).unwrap().dest() {
            if modules.contains_key(&dest) {
                modules.get_mut(&dest).unwrap().init(name.clone());
            }
        }
    }

    modules
}
