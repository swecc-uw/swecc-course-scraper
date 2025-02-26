from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypeVar

"""
Response parsing module for the DawgPath API.

This module provides data classes and parsing functions for the various
API responses from the DawgPath service.
"""

T = TypeVar("T")


def parse_search(json_data: Dict[str, Any]) -> "SearchResult":
    """
    Parse the JSON response from a DawgPath search API call.

    Args:
        json_data (Dict[str, Any]): The JSON response from the search API.

    Returns:
        SearchResult: A structured object containing the parsed search results.
    """
    course_matches_raw = json_data.get("course_matches", [])
    major_matches_raw = json_data.get("major_matches", [])
    text_matches_raw = json_data.get("text_matches", [])

    major_matches = []
    text_matches = []

    for major_match in major_matches_raw:
        major_matches.append(
            MajorMatch(
                abbr=major_match.get("abbr", ""),
                campus=major_match.get("campus", ""),
                description=major_match.get("description", ""),
                id=major_match.get("id", ""),
                is_major=major_match.get("is_major", False),
                score=major_match.get("score", 0.0),
                title=major_match.get("title", ""),
                url=major_match.get("url", ""),
            )
        )

    for text_match in text_matches_raw:
        text_matches.append(
            TextMatch(
                campus=text_match.get("campus", ""),
                description=text_match.get("description", ""),
                id=text_match.get("id", ""),
                is_course=text_match.get("is_course", False),
                is_major=text_match.get("is_major", False),
                score=text_match.get("score", 0.0),
                title=text_match.get("title", ""),
                url=text_match.get("url", ""),
            )
        )

    return SearchResult(
        course_matches=course_matches_raw,
        major_matches=major_matches,
        text_matches=text_matches,
    )


@dataclass
class MajorMatch:
    """
    Represents a major match result from the search API.

    Attributes:
        abbr: Abbreviation of the major.
        campus: Campus where the major is offered.
        description: Description of the major.
        id: Unique identifier for the major.
        is_major: Flag indicating if this is a major.
        score: Relevance score of the match.
        title: Title of the major.
        url: URL for more information about the major.
    """

    abbr: str
    campus: str
    description: str
    id: str
    is_major: bool
    score: float
    title: str
    url: str


@dataclass
class TextMatch:
    """
    Represents a text match result from the search API.

    Attributes:
        campus: Campus where the match is from.
        description: Description of the match.
        id: Unique identifier for the match.
        score: Relevance score of the match.
        title: Title of the match.
        url: URL for more information about the match.
        is_course: Optional flag indicating if this is a course.
        is_major: Optional flag indicating if this is a major.
    """

    campus: str
    description: str
    id: str
    score: float
    title: str
    url: str
    is_course: Optional[bool] = None
    is_major: Optional[bool] = None


@dataclass
class SearchResult:
    """
    Container for all search results from the search API.

    Attributes:
        course_matches: List of course matches.
        major_matches: List of major matches.
        text_matches: List of text matches.
    """

    course_matches: List[Dict[str, Any]]
    major_matches: List[MajorMatch]
    text_matches: List[TextMatch]


@dataclass
class CoursePrereqs:
    """
    Represents prerequisite information for a course.

    Attributes:
        course_id: Unique identifier for the course.
        course_title: Title of the course.
        postreqs: List of course IDs that have this course as a prerequisite.
        prereqs: List of course IDs that are prerequisites for this course.
    """

    course_id: str
    course_title: str
    postreqs: List[str]  # list of course_ids
    prereqs: List[str]  # list of course_ids


@dataclass
class CoursePrereqsResult:
    """
    Container for course prerequisite data from the API.

    Attributes:
        course_data: List of CoursePrereqs objects with prerequisite information.
        prereq_graph: Raw prerequisite graph data from the API (not processed).
    """

    course_data: List[CoursePrereqs]
    prereq_graph: Dict[str, Any]  # Graph representation of prerequisites


def parse_course_prereqs(json_data: Dict[str, Any]) -> CoursePrereqsResult:
    """
    Parse the JSON response from a DawgPath course prerequisites API call.

    Args:
        json_data (Dict[str, Any]): The JSON response from the prerequisites API.

    Returns:
        CoursePrereqsResult: A structured object containing the parsed prerequisite data.
    """
    course_data_raw = json_data.get("course_data", [])
    prereq_graph_raw = json_data.get("prereq_graph", {})

    course_data = []
    for course in course_data_raw:
        prereqs = course.get("prereqs", [])
        postreqs = course.get("postreqs", [])
        prereqs = [prereq.get("course_id", "") for prereq in prereqs]
        postreqs = [postreq.get("course_id", "") for postreq in postreqs]
        course_data.append(
            CoursePrereqs(
                course_id=course.get("course_id", ""),
                course_title=course.get("course_title", ""),
                postreqs=postreqs,
                prereqs=prereqs,
            )
        )

    return CoursePrereqsResult(
        course_data=course_data,
        prereq_graph=prereq_graph_raw,
    )
