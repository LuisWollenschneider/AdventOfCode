import { solve } from '../utils';

const YEAR = 2025;
const DAY = 3;

function parseInput(input: string): any {
    return input.split('\n').map(l => l.split('').map(Number));
}

function max_n_digits(row: number[], n: number): number {
    let s = 0;
    let idx = 0;
    for (let i = 0; i < n; i++) {
        let search_space = row.slice(idx, row.length - (n - i - 1));
        let m = Math.max(...search_space);
        s = s * 10 + m;
        idx += search_space.indexOf(m) + 1;
    }
    return s;
}


function part1(input: string): any | null {
    let inp = parseInput(input);

    let s = 0;
    for (let row of inp) {
        s += max_n_digits(row, 2);
    }

    return s;
}

function part2(input: string): any | null {
    let inp = parseInput(input);
    
    let s = 0;
    for (let row of inp) {
        s += max_n_digits(row, 12);
    }

    return s;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);