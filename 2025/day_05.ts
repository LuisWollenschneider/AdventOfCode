import { solve } from '../utils';

const YEAR = 2025;
const DAY = 5;

function parseInput(input: string): any {
    let [ranges, ids] = input.split('\n\n');
    return [
        ranges.split('\n').map(line => line.trim().split('-').map(Number)),
        ids.split('\n').map(Number)
    ];
}


function part1(input: string): any | null {
    let [ranges, ids] = parseInput(input);

    let fresh = 0;
    for (let id of ids) {
        for (let [start, end] of ranges) {
            if (id >= start && id <= end) {
                fresh++;
                break;
            }
        }
    }

    return fresh;
}

function part2(input: string): any | null {
    let [ranges, _] = parseInput(input);

    while (true) {
        let didMerge = false;
        for (let i = 0; i < ranges.length; i++) {
            let [start1, end1] = ranges[i];
            let mergedThisRound = false;
            for (let j = i + 1; j < ranges.length; j++) {
                let [start2, end2] = ranges[j];
                if (start1 <= end2 && end2 <= end1 || 
                    start1 <= start2 && start2 <= end1 ||
                    start2 <= end1 && end1 <= end2 ||
                    start2 <= start1 && start1 <= end2) {
                    ranges[i] = [Math.min(start1, start2), Math.max(end1, end2)];
                    ranges.splice(j, 1);
                    didMerge = true;
                    mergedThisRound = true;
                    break;
                }
            }
            if (mergedThisRound) {
                break;
            }
        }
        if (!didMerge) {
            break;
        }
    }

    let total = 0;
    for (let [start, end] of ranges) {
        total += end - start + 1;
    }
    return total;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);