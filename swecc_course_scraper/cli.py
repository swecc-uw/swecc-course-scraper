import argparse

from swecc_course_scraper.commands.login import command as login
from swecc_course_scraper.commands.login import load_schedule as schedule

EXPECTED_ARGS_LEN = 3


def main(args: argparse.Namespace) -> None:
    if args.login:
        login(args)
    elif args.schedule is not None:
        if len(args.schedule) == EXPECTED_ARGS_LEN:
            schedule(
                department=args.schedule[0],
                quarter=args.schedule[1],
                year=args.schedule[2],
            )
        elif len(args.schedule) == 0:
            print(schedule())
        else:
            print("Incorrect number of parameters")
    else:
        print("No command specified. Use --login to log in to DawgPath.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="Log in to DawgPath")
    parser.add_argument(
        "--schedule",
        nargs="*",
        type=str,
        help="Get schedule for department, quarter, and year",
    )
    main(parser.parse_args())
