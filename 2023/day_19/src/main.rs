use std::collections::HashMap;
use utils_rust::utils::wrapper;

const DAY: i32 = 19;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let (workflows, parts) = parse(input);
    let mut accepted_parts: Vec<Part> = Vec::new();
    let mut queue: Vec<(&Part, String)> = parts.iter().map(|part| (part, "in".to_string())).collect();
    while !queue.is_empty() {
        let (part, workflow) = queue.pop().unwrap();
        match workflows.get(workflow.as_str()).unwrap().next_workflow(&part).as_str() {
            "A" => accepted_parts.push((*part).clone()),
            "R" => {},
            wf => {
                queue.push((part, wf.to_string()));
            }
        }
    }

    accepted_parts.iter().map(|part| part.sum()).sum::<i64>().to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let (workflows, _) = parse(input);
    let mut queue: Vec<(PartRange, String)> = vec![(PartRange {
        x_min: 1,
        x_max: 4000,
        m_min: 1,
        m_max: 4000,
        a_min: 1,
        a_max: 4000,
        s_min: 1,
        s_max: 4000
    }, "in".to_string())];
    let mut accepted_parts: Vec<PartRange> = Vec::new();

    while !queue.is_empty() {
        let (part_range, workflow) = queue.pop().unwrap();
        let workflow: &Workflow = workflows.get(workflow.as_str()).unwrap();

        for (pr, wf) in workflow.translate_range(&part_range) {
            match wf.as_str() {
                "A" => accepted_parts.push(pr.clone()),
                "R" => {},
                wf => {
                    queue.push((pr, wf.to_string()));
                }
            }
        }
    }

    accepted_parts.iter().map(|part_range| part_range.size()).sum::<i64>().to_string()
}

#[derive(Clone)]
struct Part {
    x: i64,
    m: i64,
    a: i64,
    s: i64
}

impl Part {
    fn sum(&self) -> i64 {
        self.x + self.m + self.a + self.s
    }

    fn get_param(&self, param: char) -> i64 {
        match param {
            'x' => self.x,
            'm' => self.m,
            'a' => self.a,
            's' => self.s,
            _ => panic!("Invalid param: {}", param)
        }
    }
}

#[derive(Clone)]
struct PartRange {
    x_min: i64,
    x_max: i64,
    m_min: i64,
    m_max: i64,
    a_min: i64,
    a_max: i64,
    s_min: i64,
    s_max: i64
}

impl PartRange {
    fn is_valid(&self) -> bool {
        self.x_min <= self.x_max &&
        self.m_min <= self.m_max &&
        self.a_min <= self.a_max &&
        self.s_min <= self.s_max
    }

    fn size(&self) -> i64 {
        let x_size = self.x_max - self.x_min + 1;
        let m_size = self.m_max - self.m_min + 1;
        let a_size = self.a_max - self.a_min + 1;
        let s_size = self.s_max - self.s_min + 1;
        x_size * m_size * a_size * s_size
    }
}

struct Rule {
    param: char,
    cmp: char,
    value: i64,
    workflow: String,
    last: bool
}

impl Rule {
    fn is_valid(&self, part: &Part) -> bool {
        if self.last {
            return true;
        }

        match self.cmp {
            '>' => part.get_param(self.param) > self.value,
            '<' => part.get_param(self.param) < self.value,
            _ => panic!("Invalid comparison: {}", self.cmp)
        }
    }
}

struct Workflow {
    rules: Vec<Rule>,
}

impl Workflow {
    fn next_workflow(&self, part: &Part) -> String {
        for rule in &self.rules {
            if rule.is_valid(part) {
                return rule.workflow.clone();
            }
        }

        panic!("No valid rule found for part");
    }

    fn translate_range(&self, range: &PartRange) -> Vec<(PartRange, String)> {
        let mut translations: Vec<(PartRange, String)> = Vec::new();

        let mut pr = range.clone();
        for rule in &self.rules {
            if rule.last {
                translations.push((pr.clone(), rule.workflow.clone()));
                break;
            }

            let mut true_range = pr.clone();
            let mut false_range = pr.clone();

            match rule.cmp {
                '<' => {
                    match rule.param {
                        'x' => {
                            true_range.x_max = true_range.x_max.min(rule.value - 1);
                            false_range.x_min = false_range.x_min.max(rule.value);
                        },
                        'm' => {
                            true_range.m_max = true_range.m_max.min(rule.value - 1);
                            false_range.m_min = false_range.m_min.max(rule.value);
                        },
                        'a' => {
                            true_range.a_max = true_range.a_max.min(rule.value - 1);
                            false_range.a_min = false_range.a_min.max(rule.value);
                        },
                        's' => {
                            true_range.s_max = true_range.s_max.min(rule.value - 1);
                            false_range.s_min = false_range.s_min.max(rule.value);
                        },
                        _ => panic!("Invalid param: {}", rule.param)
                    };
                }
                '>' => {
                    match rule.param {
                        'x' => {
                            true_range.x_min = true_range.x_min.max(rule.value + 1);
                            false_range.x_max = false_range.x_max.min(rule.value);
                        },
                        'm' => {
                            true_range.m_min = true_range.m_min.max(rule.value + 1);
                            false_range.m_max = false_range.m_max.min(rule.value);
                        },
                        'a' => {
                            true_range.a_min = true_range.a_min.max(rule.value + 1);
                            false_range.a_max = false_range.a_max.min(rule.value);
                        },
                        's' => {
                            true_range.s_min = true_range.s_min.max(rule.value + 1);
                            false_range.s_max = false_range.s_max.min(rule.value);
                        },
                        _ => panic!("Invalid param: {}", rule.param)
                    };
                }
                _ => panic!("Invalid comparison: {}", rule.cmp)
            }

            if true_range.is_valid() {
                translations.push((true_range.clone(), rule.workflow.clone()));
            }
            if !false_range.is_valid() {
                break;
            }
            pr = false_range;
        }

        translations
    }

}

fn parse(input: &String) -> (HashMap<String, Workflow>, Vec<Part>) {
    let mut workflows: HashMap<String, Workflow> = HashMap::new();
    let mut parts: Vec<Part> = Vec::new();

    let (ws, ps) = input.split_once("\n\n").unwrap();
    for line in ws.lines() {
        let (name, rules) = line.split_once('{').unwrap();
        let rules: Vec<Rule> = rules
            .trim_end_matches('}')
            .split(",")
            .map(|rule| {
                if rule.contains(':') {
                    let (op, next_workflow) = rule.split_once(":").unwrap();
                    Rule {
                        param: op.chars().next().unwrap(),
                        cmp: op.chars().nth(1).unwrap(),
                        value: op[2..].parse::<i64>().unwrap(),
                        workflow: next_workflow.trim().to_string(),
                        last: false
                    }
                } else {
                    Rule {
                        param: 'x',
                        cmp: 'x',
                        value: 0,
                        workflow: rule.trim().to_string(),
                        last: true
                    }
                }
            })
            .collect();

        workflows.insert(name.to_string(), Workflow { rules });
    }

    for line in ps.lines() {
        let line = line.trim_start_matches('{').trim_end_matches('}');
        let params: Vec<&str> = line.split(",").collect();
        parts.push(Part {
            x: params[0][2..].parse::<i64>().unwrap(),
            m: params[1][2..].parse::<i64>().unwrap(),
            a: params[2][2..].parse::<i64>().unwrap(),
            s: params[3][2..].parse::<i64>().unwrap(),
        });
    }

    (workflows, parts)
}