from typing import Dict, List

from swecc_course_scraper.commands.schedule import (
    CURRENT_YEAR,
    EARLIEST_RECORDED_YEAR,
    VALID_QUARTERS,
)
from swecc_course_scraper.commands.schedule import (
    command as schedule_command,
)


def command(course_code: str, check_years: int = 5) -> str:
    """
    Fetches the frequence for a specified course code from multiple quarters.

    Args:
        str: The course code (e.g., "cse143", "CSE143").
        int: The number of years to check for course frequency. Default is 5.

    Returns:
        str: Lists course offering frequency.
    """

    course_department = "".join(filter(str.isalpha, course_code)).lower()
    course_number = "".join(filter(str.isdigit, course_code))
    course_code = f"{course_department}{course_number}"

    frequency: Dict[str, int] = {}
    offerings: List[str] = []
    total_quarters: int = 0

    earliest_year = max(CURRENT_YEAR - check_years + 1, EARLIEST_RECORDED_YEAR)
    for year in range(CURRENT_YEAR, earliest_year - 1, -1):
        for quarter in VALID_QUARTERS:
            total_quarters += 1
            try:
                schedule_data = schedule_command(course_department, quarter, year)
                if course_code in schedule_data:
                    frequency[quarter] = frequency.get(quarter, 0) + 1
                    offerings.append(f"{quarter} {year}")
            except (FileNotFoundError, ConnectionError):
                logging.exception(f"Error fetching schedule for {course_department} {quarter} {year}")
                continue

    result = [f"Course {course_code.upper()}:"]

    if offerings:
        result.append(
            f"Offered {len(offerings)} times for {total_quarters} quarters "
            f"in the last {check_years} years."
        )
        result.append("\nFrequency by quarter:")
        for quarter in sorted(frequency.keys()):
            result.append(f"- {quarter}: {frequency[quarter]} times")
        result.append("\nQuarters offered:")
        for offering in sorted(offerings):
            result.append(f"- {offering}")
    else:
        result.append("No offerings found for course in the time range.")

    return "\n".join(result)
