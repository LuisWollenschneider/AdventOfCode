import argparse
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Set up a new Advent of Code day directory with template files."
    )
    parser.add_argument("language", type=str, choices=["py", "ts", "cpp", "rs"], help="Programming language to use for the template.")
    parser.add_argument("year", type=int, nargs="?", default=datetime.now().year, help="The year of the Advent of Code event.")
    parser.add_argument("day", type=int, nargs="?", default=datetime.now().day, help="The day of the Advent of Code event.")
    args = parser.parse_args()

    year = args.year
    day = args.day

    if year < 2015 or year > datetime.now().year:
        raise ValueError("Year must be between 2015 and the current year.")
    if day < 1 or day > 25:
        raise ValueError("Day must be between 1 and 25.")

    day_str = f"day_{day:02d}"
    dir_path = f"{year}/{day_str}"
    test_file = f"{year}/tests/{day_str}.txt"

    os.makedirs(str(year), exist_ok=True)
    os.makedirs(f"{year}/tests", exist_ok=True)

    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("")

    if args.language == "py":
        with open(f"template_py/template.py", "r") as f:
            template = f.read()
        template = template.replace("<YEAR>", str(year)).replace("<DAY>", str(day))
        with open(f"{year}/day_{day:02d}.py", "w") as f:
            f.write(template)
    
    elif args.language == "ts":
        with open(f"template_ts/template.ts", "r") as f:
            template = f.read()
        template = template.replace("<YEAR>", str(year)).replace("<DAY>", str(day))
        with open(f"{year}/day_{day:02d}.ts", "w") as f:
            f.write(template)

    elif args.language == "cpp":
        raise NotImplementedError("C++ template setup not implemented yet.")
    
    elif args.language == "rs":
        os.makedirs(f"{year}/day_{day:02d}", exist_ok=True)
        with open(f"template_rs/Cargo.toml", "r") as f:
            cargo_template = f.read()
        cargo_template = cargo_template.replace("<DAY_PADDED>", f"{day:02d}")
        with open(f"{year}/day_{day:02d}/Cargo.toml", "w") as f:
            f.write(cargo_template)

        os.makedirs(f"{year}/day_{day:02d}/src", exist_ok=True)
        with open(f"template_rs/src/main.rs", "r") as f:
            main_template = f.read()
        main_template = main_template.replace("<YEAR>", str(year)).replace("<DAY>", str(day))
        with open(f"{year}/day_{day:02d}/src/main.rs", "w") as f:
            f.write(main_template)

    else:
        raise ValueError("Unsupported language specified.")



if __name__ == "__main__":
    main()