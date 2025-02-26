import argparse
from swecc_course_scraper.commands.login import command as login


def main(args: argparse.Namespace) -> None:
    if args.login:
        login(args)
    else:
        print("No command specified. Use --login to log in to DawgPath.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="Log in to DawgPath")

    main(parser.parse_args())
