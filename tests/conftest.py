# tests/conftest.py

import logging
import configparser
import subprocess
import time
import pytest

from typing import Dict, Generator

from playwright.sync_api import sync_playwright, Browser, Page

from src.linkedin.facade import LinkedInFacade
from src.models.job import Job
import src.logger as LOGGER

@pytest.fixture(scope="module")
def logger():
    """Provides a configured logger instance."""
    return LOGGER.get(__name__)

@pytest.fixture
def config(logger: logging.Logger) -> configparser.ConfigParser:
    """Provides a ConfigParser object initialized with config.ini."""
    logger.info("Loading configuration from pytest.ini")
    config = configparser.ConfigParser()
    config.read("pytest.ini")
    return config

@pytest.fixture(scope="session")
def test_server(request: pytest.FixtureRequest, logger: logging.Logger) -> Generator[str, None, None]:
    """Fixture to run a simple HTTP server for serving the test HTML page."""
    logger.info("Starting test HTTP server")
    process = subprocess.Popen(["python", "-m", "http.server", "--directory", "data\\tests\\"])
    time.sleep(3)
    yield "http://localhost:8000/"
    logger.info("Stopping test HTTP server")
    process.terminate()
    logger.info("Test HTTP server terminated")

@pytest.fixture(scope="module")
def playwright_browser(logger: logging.Logger) -> Generator[Browser, None, None]:
    """Fixture to set up and tear down the Playwright browser instance."""
    try:
        logger.info("Launching Playwright browser...")
        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            logger.info("Playwright browser launched successfully.")
            yield browser
            logger.info("Closing Playwright browser...")
            browser.close()
            logger.info("Playwright browser closed.")
    except Exception as e:
        logger.error(f"Failed to launch Playwright browser: {e}")
        raise

@pytest.fixture(scope="function")
def test_page(playwright_browser: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down the Playwright page instance."""
    context = playwright_browser.new_context()
    page = context.new_page()
    logger.info("Navigating to test page...")
    page.goto("http://localhost:8000/selenium_test_page.html")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()
    context.close()

@pytest.fixture(scope="function")
def playwright_page(playwright_browser: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down a Playwright page instance for tests."""
    context = playwright_browser.new_context()
    page = context.new_page()
    logger.info("Navigating to test page...")
    page.goto("about:blank")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()
    context.close()

@pytest.fixture(scope="module")
def linkedin_page(playwright_browser: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down the Playwright page instance for LinkedIn."""
    context = playwright_browser.new_context()
    page = context.new_page()
    logger.info("Navigating to LinkedIn page...")
    page.goto("https://www.linkedin.com/feed/")
    logger.info("LinkedIn page loaded successfully.")
    yield page
    page.close()
    context.close()

@pytest.fixture(scope="module")
def linkedin_facade(linkedin_page: Page) -> LinkedInFacade:
    """Provides a LinkedInFacade instance with a mocked Playwright Page."""
    return LinkedInFacade(linkedin_page)

@pytest.fixture
def test_job():
    return Job(
        title="Test Job", 
        company="Test Company", 
        location="Test Location", 
        url="about:blank"
    )

@pytest.fixture
def test_user_info() -> Dict[str, str]:
    return {
        "first_name": "Test First",
        "last_name": "Test Last",
        "email": "test@example.com",
        "phone": "123-456-7890",
        "resume_path": "/path/to/resume.pdf"
    }

@pytest.fixture
def caplog(caplog):
    """Provides a fixture to capture log output."""
    return caplog