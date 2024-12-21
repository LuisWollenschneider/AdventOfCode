from urllib import request, parse
from urllib.error import HTTPError
import re
import copy
import os
import json
from typing import Optional
import time


BLUE = "\033[94m"
LIGHT_GREEN = "\033[92m"
GREEN = "\033[32m"
PINK = "\033[95m"
DARK_ORANGE = "\033[33m"
ORANGE = "\033[31;1m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

ROOT_URL = 'https://adventofcode.com'

TEMPLATE_HEADER = {
    'Accept-Language': 'en-US,en;q=0.8', 
    'Accept-Encoding': 'none', 
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
    'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0.1; MotoG4 Build/MPI24.107-55) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36'
}

ENCODING_TYPE = 'utf-8'


class AOCMiscUtil:
    @staticmethod
    def get_input_file_url(year, day):
        global ROOT_URL
        return f"{ROOT_URL}/{year}/day/{day}/input"

    @staticmethod
    def get_question_url(year, day):
        global ROOT_URL
        return f"{ROOT_URL}/{year}/day/{day}"

    @staticmethod
    def get_answer_url(year, day):
        global ROOT_URL
        return f"{ROOT_URL}/{year}/day/{day}/answer"

    @staticmethod
    def get_cookie(cookie_file_path):
        data = None
        if not os.path.exists(cookie_file_path):
            raise Exception(f"Invalid cookie-file path - {cookie_file_path}")
        with open(cookie_file_path, 'r') as cf:
            try:
                data = json.load(cf)
            except:
                raise Exception(f"Invalid json file - {cookie_file_path}")
            
        cookie = data.get('aoc-session-cookie', None) if data else None
        if cookie is None:
            raise Exception("Invalid cookie file")

        return cookie
        
    @staticmethod
    def get_clean_response(page):
        page = re.findall(r"article>(.*)</article", page, re.DOTALL)[0]
        page = re.sub(r'<a href.*?</a>', "", page)
        page = page.replace('<p>', '').replace('</p>', '')
        return page
        

class AOCCommunicator:
    def __init__(self, usession, uname=None, debug=False):
        global TEMPLATE_HEADER
        self.headers = copy.deepcopy(TEMPLATE_HEADER)
        self.headers['Cookie'] = f'session={usession}'
        self.network_call_count = 0
        self.debug = debug
        if uname is not None:
            self.validate_session(uname.strip())

    def get_user_name(self):
        global ROOT_URL
        page = self.get_response(ROOT_URL)
        # print(page)
        match = re.search(r'div class="user">(.*?) <', page)
        if match:
            uname = match.group(1).strip()
            return uname
        return None

    def validate_session(self, uname):
        if uname == self.get_user_name():
            return True
        else:
            raise Exception("Invalid Session")
            
    def get_response(self, url, post_data=None):
        global ENCODING_TYPE
        req = request.Request(url, headers=self.headers)
        try:
            if post_data:
                post_data_raw = parse.urlencode(post_data).encode()
                res = request.urlopen(req, data=post_data_raw)
            else:
                res = request.urlopen(req)
        except HTTPError as ee:
            ss = f"Link: {url}\n"
            ss += f"is post request? {bool(post_data)}\n"
            ss += f"session-cookie: {self.headers['Cookie']}\n"
            raise Exception(ss)
            
        self.network_call_count += 1
        if self.debug:
            print(f"{GREEN}<DBG>{RESET} Network call #{self.network_call_count}")
        page = res.read().decode(ENCODING_TYPE)
        return page

    @staticmethod
    def get_test_file(year, day) -> Optional[str]:
        file_name = f"../{year}/tests/day_{day :0>2}.txt"
        if os.path.exists(file_name):
            with open(file_name, 'r') as inp_file:
                return inp_file.read()
        return None

    def run_test(self, func, level, year, day) -> None:
        inp = self.get_test_file(year, day)
        if inp is None:
            return
        file_name = f"../{year}/tests/results/day_{str(day).zfill(2)}_{level}.txt"
        if not os.path.exists(file_name):
            res = input(f"Enter test result for day {day} level {level}: ")
            with open(file_name, 'w') as res_file:
                res_file.write(res)
        else:
            with open(file_name, 'r') as inp_file:
                res = inp_file.read().strip()
        if res == "":
            return
        print(f"{BLUE}Running test for level {PINK}{level}{BLUE}...{RESET}", end=" ")
        start = time.time()
        ans = func(inp)
        end = time.time()
        print(f"{LIGHT_GREEN}Done!{RESET}")

        if ans is None:
            print(f"{DARK_ORANGE}Not Implemented!{RESET}")
            exit(1)

        if self.debug:
            print(f"{GREEN}<DBG> {DARK_ORANGE}Time taken: {PINK}{format_time(end - start)}{RESET}")
        if str(ans) == res:
            print(f"\t{LIGHT_GREEN}TEST PASSED!{RESET}")
        else:
            print(f"\t{RED}TEST FAILED!{RESET}\n"
                  f"\t\t{DARK_ORANGE}Expected: {RED}{res}{RESET}\n"
                  f"\t\t{DARK_ORANGE}Output:   {RED}{ans}{RESET}")
            exit(1)

    def get_input_file(self, year, day, force=False):
        file_name = f"../{year}/inputs/day_{day :0>2}.txt"
        if (not force) and os.path.exists(file_name):
            if self.debug:
                print(f"{GREEN}<DBG>{RESET} Input file already exists. Using cached data")
            with open(file_name, 'r') as inp_file:
                page = inp_file.read()     
        else:
            if self.debug:
                print(f"{GREEN}<DBG>{RESET} Input file doesn't exist. Fetching from AoC")
            page = self.get_response(AOCMiscUtil.get_input_file_url(year, day))
            with open(file_name, 'w') as inp_file:
                inp_file.write(page)
        return page

    def submit_answer(self, year, day, level, answer):
        url = AOCMiscUtil.get_answer_url(year, day) 
        post_data = {
            'level': level,
            'answer': str(answer)
        }
        page = self.get_response(url, post_data=post_data)
        return AOCMiscUtil.get_clean_response(page)


def create_test_file(settings: dict, level: int, content: str = "") -> None:
    def create_file(file_name: str, c: str = "") -> None:
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write(c)

    def create_test_input(year: int, day: int):
        create_file(f"../{year}/tests/day_{day :0>2}.txt")

    def create_test_result(year: int, day: int, lvl: int, c):
        create_file(f"../{year}/tests/results/day_{day:0>2}_{lvl}.txt", c)

    assert level in [1, 2], "Invalid level"
    create_test_input(settings["year"], settings["day"])
    create_test_result(settings["year"], settings["day"], level, content)


def format_time(td: float) -> str:
    res = ""
    days = int(td // (24 * 3600))
    hours = int((td % (24 * 3600)) // 3600)
    minutes = int((td % 3600) // 60)
    seconds = int(td % 60)
    milliseconds = int(td % 1 * 1e3)
    microsecond = int(td % 1e-3 * 1e6)
    nanoseconds = int(td % 1e-6 * 1e9)

    if days:
        res += f"{days}{DARK_ORANGE}d{PINK} "
    if hours or (res and any([minutes, seconds, milliseconds, microsecond, nanoseconds])):
        res += f"{hours}{DARK_ORANGE}h{PINK} "
    if minutes or (res and any([seconds, milliseconds, microsecond, nanoseconds])):
        res += f"{minutes}{DARK_ORANGE}m{PINK} "
    if seconds or (res and any([milliseconds, microsecond, nanoseconds])):
        res += f"{seconds}{DARK_ORANGE}s{PINK} "
    if milliseconds or (res and any([microsecond, nanoseconds])):
        res += f"{milliseconds}{DARK_ORANGE}ms{PINK} "
    if microsecond or (res and nanoseconds):
        res += f"{microsecond}{DARK_ORANGE}µs{PINK} "
    if nanoseconds:
        res += f"{nanoseconds}{DARK_ORANGE}ns{PINK} "
    if not res:
        res = f"{td % 1e-9 * 1e12:.3f}e-9{DARK_ORANGE}s{PINK}"
    return res


def aoc_comm(settings, level, *, debug: bool = False, test_case: bool = True, previous_attempts: list = None):
    def deco(func):
        nonlocal settings
        session_cookie = AOCMiscUtil.get_cookie(settings['cookie-path'])
        comm = AOCCommunicator(session_cookie, debug=debug)

        def wrapper():
            nonlocal comm
            nonlocal settings, level
            if test_case:
                comm.run_test(func, level, settings["year"], settings["day"])
            page = comm.get_input_file(settings['year'], settings['day'])
            print(f"{BLUE}Running level {PINK}{level}{BLUE}...{RESET}", end=" ")
            start = time.time()
            ans = func(page)
            end = time.time()
            print(f"{BLUE}Done!{RESET}")
            if debug:
                print(f"{GREEN}<DBG> {DARK_ORANGE}Time taken: {PINK}{format_time(end - start)}{RESET}")
            if previous_attempts and (ans in previous_attempts):
                print(f"{DARK_ORANGE}Answer {LIGHT_GREEN}{ans}{DARK_ORANGE} already submitted for part {PINK}{level}{RESET} ({RED}WRONG{RESET})")
                return
            if (ans is None) or ("y" != input(f"{BLUE}Submit answer {LIGHT_GREEN}{ans}{BLUE} for part {PINK}{level}{BLUE}?{RESET} ")):
                print(f"{DARK_ORANGE}Answer for part {PINK}{level}{DARK_ORANGE} not submitted{RESET}")
            else:
                response = comm.submit_answer(settings['year'], settings['day'], level, ans)
                resp = f"{ORANGE}Response from AoC:{RESET} "
                if "That's the right answer!" in response:
                    print(resp + f"{YELLOW}That's the right answer!{RESET}")
                elif "That's not the right answer" in response:
                    print(resp + f"{RED}That's not the right answer!{RESET}")
                elif "Did you already complete it?" in response:
                    print(resp + f"{DARK_ORANGE}Already submitted!{RESET}")
                elif "You gave an answer too recently" in response:
                    print(resp + f"{RED}You gave an answer too recently{RESET}")
                    wait_time = response.split("trying again.")[1].strip()
                    print(f"{DARK_ORANGE}{wait_time}{RESET}")
                else:
                    print(resp + f"{RED}Unknown response:{RESET}")
                    print(response)
            print()
        return wrapper
    return deco
