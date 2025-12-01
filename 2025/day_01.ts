import { solve } from '../utils';

const YEAR = 2025;
const DAY = 1;

function parseInput(input: string): any {
    return input.split('\n').map(l =>
        [l[0], Number(l.slice(1))]
    );
}


function part1(input: string): any | null {
    let inp = parseInput(input);
    let s = 50;
    let c = 0;
    for (let [dir, val] of inp) {
        s = (s + (dir === "L" ? -val : val)) % 100;
        c += s === 0 ? 1 : 0;
    }

    return c;
}

function part2(input: string): any | null {
    let inp = parseInput(input);
    let s = 50;
    let c = 0;
    for (let [dir, val] of inp) {
        while (val-- > 0) {
            s = ((s + (dir === "L" ? -1 : 1)) % 100 + 100) % 100;
            c += s === 0 ? 1 : 0;
        }
    }

    return c;
}

solve(part1, YEAR, DAY, 1);
solve(part2, YEAR, DAY, 2);