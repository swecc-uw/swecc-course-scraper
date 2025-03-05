from datetime import datetime

import requests

SCHEDULE = "https://www.washington.edu/students/timeschd/"
EARLIEST_RECORDED_YEAR = 2003
CURRENT_YEAR = datetime.now().year


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

    if quarter not in ["WIN", "SPR", "SUM", "AUT"]:
        raise ValueError("Quarter must be WIN, SPR, SUM, or AUT")

    try:
        year = int(year)
    except ValueError as err:
        raise ValueError("Year must be a number.") from err

    if year < EARLIEST_RECORDED_YEAR or year > CURRENT_YEAR:
        raise ValueError(
            f"Year must be between {EARLIEST_RECORDED_YEAR} and {CURRENT_YEAR}"
        )

    res = requests.get(f"{SCHEDULE}{quarter}{year}/{department}.html")
    return res.text
