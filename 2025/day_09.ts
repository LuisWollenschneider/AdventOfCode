import { solve } from '../utils';

const YEAR = 2025;
const DAY = 9;

function parseInput(input: string): any {
    return input.split('\n').map(line => line.trim().split(',').map(Number));
}


function part1(input: string): any | null {
    let inp = parseInput(input);

    let area = 0;
    for (let i = 0; i < inp.length; i++) {
        let [x1, y1] = inp[i];
        for (let j = i + 1; j < inp.length; j++) {
            let [x2, y2] = inp[j];
            area = Math.max((Math.abs(x2 - x1) + 1) * (Math.abs(y2 - y1) + 1), area);
        }
    }

    return area;
}

/*
Not a very efficient solution, but works...
*/
function part2(input: string): any | null {
    let inp: [number, number][] = parseInput(input);

    let edges: [number, number, number, number][] = [];
    let x_min = Infinity;
    let x_max = -Infinity;
    let y_min = Infinity;
    let y_max = -Infinity;
    for (let i = 0; i < inp.length; i++) {
        let [x1, y1] = inp[i];
        x_min = Math.min(x_min, x1);
        x_max = Math.max(x_max, x1);
        y_min = Math.min(y_min, y1);
        y_max = Math.max(y_max, y1);
        let [x2, y2] = inp[(i + 1) % inp.length];
        edges.push([x1, y1, x2, y2]);
    }

    let inside = (x: number, y: number): boolean => {
        // points on edge are considered inside
        let count = 0;
        for (let [x1, y1, x2, y2] of edges) {
            if (y1 == y2) {
                // horizontal edge
                if (y == y1 && x >= Math.min(x1, x2) && x <= Math.max(x1, x2)) {
                    return true;
                }
                continue;
            }
            if (y < Math.min(y1, y2) || y >= Math.max(y1, y2)) {
                continue;
            }
            // x1 == x2 vertical edge
            let x_edge = x1;
            if (x == x_edge) {
                return true;
            }
            if (x < x_edge) {
                count++;
            }
        }
        return count % 2 == 1;
    };

    let candidates: {a: number, x1: number, y1: number, x2: number, y2: number}[] = [];
    for (let i = 0; i < inp.length; i++) {
        let [x1, y1] = inp[i];
        for (let j = i + 1; j < inp.length; j++) {
            let [x2, y2] = inp[j];
            let a = (Math.abs(x2 - x1) + 1) * (Math.abs(y2 - y1) + 1);
            candidates.push({a, x1, y1, x2, y2});
        }
    }
    candidates.sort((a, b) => b.a - a.a);

    let filter_candidates = (x: number, y: number) => {
        candidates = candidates.filter(({x1, y1, x2, y2}) => {
            return !(x >= Math.min(x1, x2) && x <= Math.max(x1, x2) &&
                     y >= Math.min(y1, y2) && y <= Math.max(y1, y2));
        });
    };

    while (candidates.length > 0) {
        let {a, x1, y1, x2, y2} = candidates[0];

        let all_inside = true;
        // only check corners and edges
        for (let x = Math.min(x1, x2); x <= Math.max(x1, x2); x++) {
            if (!inside(x, y1)) {
                all_inside = false;
                filter_candidates(x, y1);
                break;
            }
            if (!inside(x, y2)) {
                all_inside = false;
                filter_candidates(x, y2);
                break;
            }
        }
        if (!all_inside) continue;
        for (let y = Math.min(y1, y2); y <= Math.max(y1, y2); y++) {
            if (!inside(x1, y)) {
                all_inside = false;
                filter_candidates(x1, y);
                break;
            }
            if (!inside(x2, y)) {
                all_inside = false;
                filter_candidates(x2, y);
                break;
            }
        }
        
        if (!all_inside) continue;

        // follow edges inside and check surroundings for wholes
        for (let [ex1, ey1, ex2, ey2] of edges) {
            if (Math.max(x1, x2) < Math.min(ex1, ex2) ||
                Math.min(x1, x2) > Math.max(ex1, ex2) ||
                Math.max(y1, y2) < Math.min(ey1, ey2) ||
                Math.min(y1, y2) > Math.max(ey1, ey2)) {
                continue; // does not enter
            }

            for (let x = Math.min(ex1, ex2); x <= Math.max(ex1, ex2); x++) {
                for (let y = Math.min(ey1, ey2); y <= Math.max(ey1, ey2); y++) {
                    for (let dx = -1; dx <= 1; dx++) {
                        for (let dy = -1; dy <= 1; dy++) {
                            if (Math.abs(dx) + Math.abs(dy) != 1) continue;
                            let nx = x + dx;
                            let ny = y + dy;
                            if (nx < Math.min(x1, x2) || nx > Math.max(x1, x2) ||
                                ny < Math.min(y1, y2) || ny > Math.max(y1, y2)) {
                                if (!inside(nx, ny)) {
                                    all_inside = false;
                                    filter_candidates(nx, ny);
                                    break;
                                }
                            }
                        }
                        if (!all_inside) break;
                    }
                    if (!all_inside) break;
                }
                if (!all_inside) break;
            }
            
        }

        return a;
    }

    return null;
}

await solve(part1, YEAR, DAY, 1);
await solve(part2, YEAR, DAY, 2);