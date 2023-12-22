use utils_rust::utils::wrapper;

const DAY: i32 = 22;
const YEAR: i32 = 2023;

#[warn(unused_variables)]
fn main() {
    wrapper(part_1, YEAR, DAY, 1);
    wrapper(part_2, YEAR, DAY, 2);
}

#[allow(unused_variables)]
fn part_1(input: &String) -> String {
    let mut bricks = parse(input);

    let min_x = bricks.iter().map(|b| b.start.x.min(b.end.x)).min().unwrap();
    let min_y = bricks.iter().map(|b| b.start.y.min(b.end.y)).min().unwrap();
    let max_x = bricks.iter().map(|b| b.start.x.max(b.end.x)).max().unwrap();
    let max_y = bricks.iter().map(|b| b.start.y.max(b.end.y)).max().unwrap();

    simulate_falling(&mut bricks, ((min_x, max_x), (min_y, max_y)));

    let mut non_supporting_bricks = 0;
    for brick_idx in 0..bricks.len() {
        let mut other_bricks: Vec<Brick> = bricks.clone();
        other_bricks.remove(brick_idx);

        if simulate_falling(&mut other_bricks, ((min_x, max_x), (min_y, max_y))) == 0 {
            non_supporting_bricks += 1;
        }
    }

    non_supporting_bricks.to_string()
}

#[allow(unused_variables)]
fn part_2(input: &String) -> String {
    let mut bricks = parse(input);

    let min_x = bricks.iter().map(|b| b.start.x.min(b.end.x)).min().unwrap();
    let min_y = bricks.iter().map(|b| b.start.y.min(b.end.y)).min().unwrap();
    let max_x = bricks.iter().map(|b| b.start.x.max(b.end.x)).max().unwrap();
    let max_y = bricks.iter().map(|b| b.start.y.max(b.end.y)).max().unwrap();

    simulate_falling(&mut bricks, ((min_x, max_x), (min_y, max_y)));

    let mut falling_bricks = 0;
    for brick_idx in 0..bricks.len() {
        let mut other_bricks: Vec<Brick> = bricks.clone();
        other_bricks.remove(brick_idx);

        falling_bricks += simulate_falling(&mut other_bricks, ((min_x, max_x), (min_y, max_y)));
    }

    falling_bricks.to_string()
}

#[derive(Clone)]
struct Coordinate {
    x: i64,
    y: i64,
    z: i64,
}

#[derive(Clone)]
struct Brick {
    start: Coordinate,
    end: Coordinate
}


fn simulate_falling(bricks: &mut Vec<Brick>, grid_size: ((i64, i64), (i64, i64))) -> u64 {
    let ((min_x, max_x), (min_y, max_y)) = grid_size;

    // top view of heights
    // 2D array of z coordinates, init 0's
    let mut z_map: Vec<Vec<i64>> = vec![vec![0; (max_x - min_x + 1) as usize]; (max_y - min_y + 1) as usize];

    let mut fallen_bricks: u64 = 0;
    for brick in bricks.iter_mut() {
        let low = brick.start.z.min(brick.end.z);

        // find highest point to place brick
        let mut peak = 0;
        for x in brick.start.x.min(brick.end.x)..=brick.start.x.max(brick.end.x) {
            for y in brick.start.y.min(brick.end.y)..=brick.start.y.max(brick.end.y) {
                peak = peak.max(z_map[(y - min_y) as usize][(x - min_x) as usize])
            }
        }

        // how far down does the brick fall?
        let z_diff = low - peak - 1;

        // if the brick falls, count it
        if z_diff != 0 {
            fallen_bricks += 1;
        }

        // new height
        brick.start.z -= z_diff;
        brick.end.z -= z_diff;

        // highest point of brick
        let high = brick.start.z.max(brick.end.z);

        // new high points in top view
        for x in brick.start.x.min(brick.end.x)..=brick.start.x.max(brick.end.x) {
            for y in brick.start.y.min(brick.end.y)..=brick.start.y.max(brick.end.y) {
                z_map[(y - min_y) as usize][(x - min_x) as usize] = high;
            }
        }
    }

    fallen_bricks
}

fn parse_coordinate(input: &str) -> Coordinate {
    let (x, input) = input.split_once(',').unwrap();
    let (y, z) = input.split_once(',').unwrap();
    Coordinate {
        x: x.parse().unwrap(),
        y: y.parse().unwrap(),
        z: z.parse().unwrap(),
    }
}

fn parse(input: &String) -> Vec<Brick> {
    let mut bricks: Vec<Brick> = input.lines()
        .map(|line| line.split_once('~').unwrap())
        .map(|(start, end)| {
            Brick {
                start: parse_coordinate(start),
                end: parse_coordinate(end)
            }
        })
        .collect();

    // sort bricks by lowest z coordinate
    // this way the falling simulation can always move the next brick as far down as possible
    bricks.sort_by(|a, b| a.start.z.min(a.end.z).cmp(&b.start.z.min(b.end.z)));

    bricks
}