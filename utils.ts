import * as fs from 'fs';

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

export async function solve(part_func: (input: string) => any | null, year: number, day: number, part: number): void {
    const testFilePath = `${year}/tests/day_${String(day).padStart(2, '0')}.txt`;
    if (!fs.existsSync(testFilePath)) {
        console.error(`Test file not found: ${testFilePath}`);
        process.exit(1);
    }
    const testResultPath = `${year}/tests/results/day_${String(day).padStart(2, '0')}_${part}.txt`;
    if (!fs.existsSync(testResultPath)) {
        // read from stdin and write to test result file
        const line = await console[0];
        console.log(`Test result file not found: ${testResultPath}`);
        console.log('Please provide the expected output for the test input:');
        const stdinBuffer = fs.readFileSync(0, 'utf-8');
        fs.writeFileSync(testResultPath, stdinBuffer.trim());
    }
    const testInput = fs.readFileSync(testFilePath, 'utf-8');
    const expectedOutput = fs.readFileSync(testResultPath, 'utf-8').trim();

    const testOutput = part_func(testInput);
    if (testOutput === null) {
        console.error('Part function returned null');
        process.exit(1);
    }
    if (String(testOutput).trim() !== expectedOutput) {
        console.error(`${RED}TEST FAILED${RESET}`);
        console.error(`Expected: ${expectedOutput}`);
        console.error(`Got:      ${testOutput}`);
        process.exit(1);
    } else {
        console.log(`${GREEN}TEST PASSED${RESET}`);
    }

    const inputFilePath = `${year}/inputs/day_${String(day).padStart(2, '0')}.txt`;
    if (!fs.existsSync(inputFilePath)) {
        console.error(`Input file not found: ${inputFilePath}`);
        process.exit(1);
    }
    const input = fs.readFileSync(inputFilePath, 'utf-8');
    const output = part_func(input);
    if (output === null) {
        console.error('Part function returned null on actual input');
        process.exit(1);
    }
    console.log(`${YELLOW}Output:${RESET} ${output}`);
}