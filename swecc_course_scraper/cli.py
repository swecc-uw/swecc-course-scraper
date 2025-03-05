import argparse

from swecc_course_scraper.commands.login import command as login
from swecc_course_scraper.commands.schedule import command as schedule


def main(args: argparse.Namespace) -> None:
    try:
        if args.login:
            login(args)
        elif args.schedule:
            department, quarter, year = args.schedule
            print(schedule(department, quarter, year))
        else:
            print("No command specified. Use --help to show all commands.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="Log in to DawgPath")
    parser.add_argument(
        "--schedule",
        nargs=3,
        metavar=("DEPARTMENT", "QUARTER", "YEAR"),
        type=str,
        help="Get previous quarters schedules. e.g.: --schedule cse WIN 2023",
    )
    main(parser.parse_args())
