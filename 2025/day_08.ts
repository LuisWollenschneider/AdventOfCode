import { solve } from '../utils';

const YEAR = 2025;
const DAY = 8;

function parseInput(input: string): any {
    return input.split('\n').map(line => {
        let [x, y, z] = line.split(',').map(Number);
        return { x: x, y: y, z: z };
    });
}


function distance(a: { x: number, y: number, z: number }, b: { x: number, y: number, z: number }): number {
    return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2);
}


function part1(input: string): any | null {
    let boxes = parseInput(input);

    let cs: Set<number>[] = [];
    let map: Map<number, number> = new Map();

    let ds: [number, number, number][] = [];
    for (let i = 0; i < boxes.length; i++) {
        cs.push(new Set<number>([i]));
        map.set(i, i);
        for (let j = i + 1; j < boxes.length; j++) {
            let d = distance(boxes[i], boxes[j]);
            ds.push([d, i, j]);
        }
    }
    ds.sort((a, b) => a[0] - b[0]);

    let c = boxes.length === 20 ? 10 : 1000;
    for (let [d, i, j] of ds) {
        if (c-- <= 0) break;
        let ci = map.get(i);
        let cj = map.get(j);
        if (ci !== cj) {
            let setI = cs[ci!];
            let setJ = cs[cj!];
            for (let v of setJ) {
                setI.add(v);
                map.set(v, ci!);
            }
            cs[cj!] = new Set<number>();
        }
    }

    let largestCircuits = cs.filter(s => s.size > 0).sort((a, b) => b.size - a.size).slice(0, 3);
    let totalBoxes = largestCircuits.reduce((prod, circuit) => prod * circuit.size, 1);

    return totalBoxes;
}

function part2(input: string): any | null {
    let boxes = parseInput(input);

    let cs: Set<number>[] = [];
    let map: Map<number, number> = new Map();

    let ds: [number, number, number][] = [];
    for (let i = 0; i < boxes.length; i++) {
        cs.push(new Set<number>([i]));
        map.set(i, i);
        for (let j = i + 1; j < boxes.length; j++) {
            let d = distance(boxes[i], boxes[j]);
            ds.push([d, i, j]);
        }
    }
    ds.sort((a, b) => a[0] - b[0]);

    for (let [d, i, j] of ds) {
        let ci = map.get(i);
        let cj = map.get(j);
        if (ci !== cj) {
            let setI = cs[ci!];
            let setJ = cs[cj!];
            for (let v of setJ) {
                setI.add(v);
                map.set(v, ci!);
            }
            cs[cj!] = new Set<number>();
        }

        if (cs.filter(s => s.size > 0).length === 1) {
            return boxes[i].x * boxes[j].x;
        }
    }

    return null;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);