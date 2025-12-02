import { solve } from '../utils';

const YEAR = 2025;
const DAY = 2;

function parseInput(input: string): any {
    return input.split(',').map(e => e.split('-').map(Number));
}


function valid_1(x: number): boolean {
    let s = x.toString();
    if (s.length % 2 === 1) return true;
    let mid = s.length / 2;
    let left = s.slice(0, mid);
    let right = s.slice(mid);
    return left !== right;
}

function part1(input: string): any | null {
    let inp = parseInput(input);

    let s = 0;
    for (let [a, b] of inp) {
        for (let i = a; i <= b; i++) {
            if (!valid_1(i)) {
                s += i;
            }
        }
    }
    return s;
}

function valid_2(x: number): boolean {
    let s = x.toString();
    for (let i = 1; i < s.length; i++) {
        if (s.length % i !== 0) continue;
        let v = false;
        for (let j = 0; j < s.length - i; j += i) {
            let part = s.slice(j, j + i);
            let next_part = s.slice(j + i, j + 2 * i);
            if (part !== next_part) {
                v = true;
                break;
            }
        }
        if (!v) return false;
    }
    return true;
}

function part2(input: string): any | null {
    let inp = parseInput(input);

    let s = 0;
    for (let [a, b] of inp) {
        for (let i = a; i <= b; i++) {
            if (!valid_2(i)) {
                s += i;
            }
        }
    }
    return s;
}

solve(part1, YEAR, DAY, 1);
solve(part2, YEAR, DAY, 2);