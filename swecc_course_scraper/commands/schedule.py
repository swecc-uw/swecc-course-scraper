from datetime import datetime

import requests

SCHEDULE = "https://www.washington.edu/students/timeschd/"
EARLIEST_RECORDED_YEAR = 2003
CURRENT_YEAR = datetime.now().year
VALID_QUARTERS = ["WIN", "SPR", "SUM", "AUT"]


def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of the given UW time schedule webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The raw HTML content of the webpage.

    Raises:
        FileNotFoundError: If the page does not exist (404).
        ConnectionError: If there is a network issue.
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except requests.exceptions.HTTPError as e:
        raise FileNotFoundError(f"Page not found or no courses available: \n{e}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Unable to connect to {url}: \n{e}") from e


def command(department: str, quarter: str, year: int) -> str:
    """
    Returns the text of the schedule webpage for the given department, quarter, and year.

    Args:
        str: The department code (e.g., "cse").
        str: The quarter code (e.g., "WIN").
        int: The year code (e.g., 2023).

    Returns:
        str: The raw HTML content as text of the webpage.

    Raises:
        ValueError: If the quarter is not one of WIN, SPR, SUM, or AUT.
        ValueError: Invalid year
    """

    department = department.lower()
    quarter = quarter.upper()

    if quarter not in VALID_QUARTERS:
        raise ValueError("Quarter must be WIN, SPR, SUM, or AUT")

    try:
        year = int(year)
    except ValueError as err:
        raise ValueError("Year must be a number.") from err

    if year < EARLIEST_RECORDED_YEAR or year > CURRENT_YEAR:
        raise ValueError(
            f"Year must be between {EARLIEST_RECORDED_YEAR} and {CURRENT_YEAR}"
        )

    return fetch_html(f"{SCHEDULE}{quarter}{year}/{department}.html")
