import { solve } from '../utils';

const YEAR = 2025;
const DAY = 6;

function parseInput(input: string): any {
    return input.split('\n').map(line => line.trim().split(' ').filter(c => c.length > 0));
}


function part1(input: string): any | null {
    let inp = parseInput(input);
    let s = 0;
    for (let i = 0; i < inp[0].length; i++) {
        let ns = [];
        for (let j = 0; j < inp.length - 1; j++) {
            ns.push(Number(inp[j][i]));
        }
        if (inp[inp.length - 1][i] === '*') {
            s += ns.reduce((a, b) => a * b, 1);
        } else if (inp[inp.length - 1][i] === '+') {
            s += ns.reduce((a, b) => a + b, 0);
        }
    }
    return s;
}

function part2(input: string): any | null {
    let s = 0;
    let lines = input.split('\n');
    for (let j = 0; j < lines.length; j++) {
        lines[j] += ' ';
    }
    let ns = [];
    let op = null;
    for (let i = 0; i < lines[0].length; i++) {
        let n = '';
        for (let j = 0; j < lines.length - 1; j++) {
            n += lines[j][i];
        }
        if (op === null) {
            op = lines[lines.length - 1][i];
        }
        if (n.trim().length > 0) {
            ns.push(Number(n));
        } else {
            if (op === '*') {
                s += ns.reduce((a, b) => a * b, 1);
            } else if (op === '+') {
                s += ns.reduce((a, b) => a + b, 0);
            }
            ns = [];
            op = null;
        }
    }

    return s;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);