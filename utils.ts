import * as fs from 'fs';

const BLUE = "\x1b[94m";
const RED = "\x1b[91m";
const GREEN = "\x1b[32m";
const LIGHT_GREEN = "\x1b[92m";
const YELLOW = "\x1b[93m";
const ORANGE = "\x1b[31;1m";
const PINK = "\x1b[95m";
const DARK_ORANGE = "\x1b[33m";
const RESET = "\x1b[0m";

const ROOT_URL = 'https://adventofcode.com';

function getCookie(): string {
    const data = fs.readFileSync('aoc_cookie.json', 'utf-8');
    const json = JSON.parse(data);
    return json['aoc-session-cookie'];
}

async function fetchInput(year: number, day: number): Promise<string> {
    console.log(`${YELLOW}Fetching input for ${PINK}${day}${YELLOW}...${RESET}`);

    let filePath = `${year}/inputs/day_${String(day).padStart(2, '0')}.txt`;
    let url = `${ROOT_URL}/${year}/day/${day}/input`;
    let cookie = getCookie();

    const response = await fetch(url, {
        headers: {
            'Cookie': `session=${cookie}`,
        },
    });

    if (!response.ok) {
        console.error(`${RED}Failed to fetch input: ${response.status} ${response.statusText}${RESET}`);
        process.exit(1);
    }

    const input = await response.text();
    fs.writeFileSync(filePath, input);
    return input;
}

async function submitAnswer(year: number, day: number, part: number, answer: string): Promise<void> {
    let url = `${ROOT_URL}/${year}/day/${day}/answer`;
    let cookie = getCookie();

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Cookie': `session=${cookie}`,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `level=${part}&answer=${encodeURIComponent(answer)}`,
    });

    if (!response.ok) {
        console.error(`${RED}Failed to submit answer: ${response.status} ${response.statusText}${RESET}`);
        process.exit(1);
    }

    const text = await response.text();
    if (text.includes('That\'s the right answer!')) {
        console.log(`${YELLOW}That's the right answer!${RESET}`);
    } else if (text.includes('That\'s not the right answer.')) {
        console.log(`${RED}That's not the right answer!${RESET}`);
    } else if (text.includes('Did you already complete it?')) {
        console.log(`${DARK_ORANGE}Already submitted!${RESET}`);
    } else {
        console.log(`${RED}Unknown response:${RESET}`);
        console.log(text);
    }
}

export async function solve(part_func: (input: string) => any | null, year: number, day: number, part: number): void {
    const testFilePath = `${year}/tests/day_${String(day).padStart(2, '0')}.txt`;
    if (!fs.existsSync(testFilePath)) {
        console.error(`Test file not found: ${testFilePath}`);
        process.exit(1);
    }
    const testResultPath = `${year}/tests/results/day_${String(day).padStart(2, '0')}_${part}.txt`;
    if (!fs.existsSync(testResultPath)) {
        // prompt user for expected result
        process.stdout.write(`${BLUE}Enter expected result for part ${PINK}${part}${BLUE}:${RESET}`);
        const expectedOutput = await new Promise<string>((resolve) => {
            process.stdin.once('data', (data) => {
                resolve(data.toString().trim());
            });
        });
        if (expectedOutput.length === 0) {
            console.error(`${RED}Expected output cannot be empty!${RESET}`);
            process.exit(1);
        }
        fs.writeFileSync(testResultPath, expectedOutput);
    }
    const testInput = fs.readFileSync(testFilePath, 'utf-8');
    const expectedOutput = fs.readFileSync(testResultPath, 'utf-8').trim();

    // no new line at the end of expected output
    console.group();
    process.stdout.write(`${BLUE}Running tests for part ${PINK}${part}${BLUE}...${RESET}`);

    const testOutput = part_func(testInput);

    console.log(`${GREEN}Done!${RESET}`);
    console.groupEnd();

    if (testOutput === null) {
        console.log(`${DARK_ORANGE}Not implemented!${RESET}`);
        process.exit(1);
    }
    if (String(testOutput).trim() === expectedOutput) {
        console.log(`\t${GREEN}TEST PASSED${RESET}`);
    } else {
        console.error(`\t${RED}TEST FAILED${RESET}`);
        console.error(`\t\tExpected: ${expectedOutput}`);
        console.error(`\t\tGot:      ${testOutput}`);
        process.exit(1);
    }

    const inputFilePath = `${year}/inputs/day_${String(day).padStart(2, '0')}.txt`;
    if (!fs.existsSync(inputFilePath)) {
        await fetchInput(year, day);
    }

    const input = fs.readFileSync(inputFilePath, 'utf-8').trim();
    const output = part_func(input);
    if (output === null) {
        console.error('Part function returned null on actual input');
        process.exit(1);
    }
    console.log(`${BLUE}Submit answer ${LIGHT_GREEN}${output}${BLUE} for part ${PINK}${part}${BLUE}? (y/n)${RESET}`);
    const answer = await new Promise<string>((resolve) => {
        process.stdin.once('data', (data) => {
            resolve(data.toString().trim());
        });
    });

    if (answer.toLowerCase() === 'y') {
        await submitAnswer(year, day, part, String(output));
    } else {
        console.log(`${YELLOW}Answer not submitted.${RESET}`);
    }

    console.log();
}