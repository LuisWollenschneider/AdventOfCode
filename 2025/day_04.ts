import { solve } from '../utils';

const YEAR = 2025;
const DAY = 4;

function parseInput(input: string): any {
    return input.split('\n').map(line => line.trim().split('').map((c) => c === '@' ? 1 : 0));
}


function neighbors(x: number, y: number, grid: number[][]): number[] {
    let vs = [];
    for (let dx of [-1, 0, 1]) {
        for (let dy of [-1, 0, 1]) {
            if (dx === 0 && dy === 0) continue;
            let nx = x + dx;
            let ny = y + dy;
            if (nx >= 0 && ny >= 0 && ny < grid.length && nx < grid[ny].length) {
                vs.push(grid[ny][nx]);
            }
        }
    }
    return vs;
}

function accessable(grid: number[][]): [number, number][] {
    let as: [number, number][] = [];
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[y].length; x++) {
            if (grid[y][x] === 0) continue;
            if (neighbors(x, y, grid).reduce((a, b) => a + b, 0) < 4) {
                as.push([x, y]);
            }
        }
    }
    return as;
}


function part1(input: string): any | null {
    let inp = parseInput(input);

    return accessable(inp).length;
}

function part2(input: string): any | null {
    let inp = parseInput(input);

    let s = 0;
    while (true) {
        let acc = accessable(inp);
        if (acc.length === 0) {
            break;
        }
        s += acc.length;
        for (let [x, y] of acc) {
            inp[y][x] = 0;
        }
    }

    return s;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);