use utils_rust::utils::wrapper;

const DAY: i32 = 24;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let hailstones = parse(input);

    let min_coord: f64;
    let max_coord: f64;
    if hailstones.len() == 5 {
        min_coord = 7f64;
        max_coord = 27f64;
    } else {
        min_coord = 200000000000000f64;
        max_coord = 400000000000000f64;
    }

    let mut res = 0;
    for (i, a) in hailstones.iter().enumerate() {
        for b in hailstones.iter().skip(i + 1) {
            let (x, y) = intersection(a, b);


            if x == 0.0 && y == 0.0 {
                continue;
            }
            // println!("({}, {})", x, y);

            if x < min_coord || x > max_coord {
                continue;
            }

            if y < min_coord || y > max_coord {
                continue;
            }

            res += 1;
        }
    }

    res.to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    "".to_string()
}

fn intersection(a: &Hailstone, b: &Hailstone) -> (f64, f64) {
    let d = b.vy * a.vx - b.vx * a.vy;
    let dx = a.x - b.x;
    let dy = a.y - b.y;
    let cpa = b.vx * dy - b.vy * dx;
    let cpb = a.vx * dy - a.vy * dx;

    if d == 0.0 {
        return (0.0, 0.0);
    }

    let tx = cpa / d;
    let ty = cpb / d;

    if tx < 0.0 || ty < 0.0 {
        return (0.0, 0.0);
    }

    (a.x + tx * a.vx,
     a.y + tx * a.vy)
}

#[derive(PartialEq)]
struct Hailstone {
    x: f64,
    y: f64,
    z: f64,
    vx: f64,
    vy: f64,
    vz: f64,
}

fn parse(input: &String) -> Vec<Hailstone> {
    input.lines()
        .map(|line| line.split_once(" @ ").unwrap())
        .map(|(pos, vel)| {
            let pos = pos.splitn(3, ',').collect::<Vec<&str>>();
            let vel = vel.splitn(3, ',').collect::<Vec<&str>>();
            let x = pos[0].trim().parse::<f64>().unwrap();
            let y = pos[1].trim().parse::<f64>().unwrap();
            let z = pos[2].trim().parse::<f64>().unwrap();
            let vx = vel[0].trim().parse::<f64>().unwrap();
            let vy = vel[1].trim().parse::<f64>().unwrap();
            let vz = vel[2].trim().parse::<f64>().unwrap();
            Hailstone { x, y, z, vx, vy, vz }
        })
        .collect::<Vec<Hailstone>>()
}