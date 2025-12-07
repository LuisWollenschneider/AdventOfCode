import { solve } from '../utils';

const YEAR = 2025;
const DAY = 7;

function parseInput(input: string): any {
    return input.split('\n').map(line => line.trim().split(''));
}


function part1(input: string): any | null {
    let inp = parseInput(input);

    let beams: Set<number> = new Set();
    for (let x = 0; x < inp[0].length; x++) {
        if (inp[0][x] === 'S') {
            beams.add(x);
        }
    }

    let s = 0;
    for (let y = 0; y < inp.length; y++) {
        let newBeams: Set<number> = new Set();
        for (let beamX of beams) {
            if (inp[y]?.[beamX] === '^') {
                newBeams.add(beamX - 1);
                newBeams.add(beamX + 1);
                s++;
            } else {
                newBeams.add(beamX);
            }
        }
        beams = newBeams;
    }

    return s;
}

function part2(input: string): any | null {
    let inp = parseInput(input);

    let beams: Map<number, number> = new Map();
    for (let x = 0; x < inp[0].length; x++) {
        if (inp[0][x] === 'S') {
            beams.set(x, (beams.get(x) || 0) + 1);
        }
    }

    for (let y = 0; y < inp.length; y++) {
        let newBeams: Map<number, number> = new Map();
        for (let [beamX, n] of beams) {
            if (inp[y]?.[beamX] === '^') {
                newBeams.set(beamX - 1, (newBeams.get(beamX - 1) || 0) + n);
                newBeams.set(beamX + 1, (newBeams.get(beamX + 1) || 0) + n);
            } else {
                newBeams.set(beamX, (newBeams.get(beamX) || 0) + n);
            }
        }
        beams = newBeams;
    }

    return Array.from(beams.values()).reduce((a, b) => a + b, 0);
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);