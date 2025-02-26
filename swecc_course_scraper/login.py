import requests
from requests.sessions import Session
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

ROOT = "https://dawgpath.uw.edu"


def load_webdriver(url: str = ROOT) -> WebDriver:
    """
    Initialize and return a Chrome WebDriver instance.

    Args:
        url (str): The URL to navigate to. Defaults to ROOT.

    Returns:
        WebDriver: An initialized Chrome WebDriver instance.
    """
    driver = webdriver.Chrome()
    driver.get("")
    return driver


def get_current_http_session(driver: WebDriver) -> Session:
    """
    Extract cookies from the WebDriver and create a requests Session with those cookies.

    Args:
        driver (WebDriver): The WebDriver instance with active cookies.

    Returns:
        Session: A requests Session object with cookies from the WebDriver.
    """
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session


def example() -> None:
    """
    Example function demonstrating the workflow of logging in and making an API request.

    This function:
    1. Loads a WebDriver
    2. Waits for the user to log in manually
    3. Extracts the session cookies
    4. Makes an API request to search for "math" courses

    Returns:
        Dict[str, Any]: The JSON response from the API request.
    """
    driver = load_webdriver()

    input("Press any key to continue after logging in...")
    session = get_current_http_session(driver)

    res = requests.get(
        "https://dawgpath.uw.edu/api/v1/search/?search_string=math",
        cookies=session.cookies,
    )
    print(res.json())
