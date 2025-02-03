# tests/conftest.py

import logging
import configparser
import subprocess
import time
import pytest
from typing import Generator
from playwright.sync_api import sync_playwright, Browser, Page

from src.constants.linkedin import LinkedInConstants
from src.facade import Facade
from src.models.job import Job
import src.logger as LOGGER

@pytest.fixture(scope="module")
def config() -> configparser.ConfigParser:
    """Provides a ConfigParser object initialized with config.ini."""
    logger = LOGGER.get(__name__)
    logger.info("Loading configuration from pytest.ini")
    config = configparser.ConfigParser()
    config.read("pytest.ini")
    return config

@pytest.fixture(scope="module")
def logger(config: configparser.ConfigParser) -> logging.Logger:
    """Provides a configured logger instance."""
    LOGGER.set_output_path(config.get("general", "log_file_path"))
    return LOGGER.get(__name__)

@pytest.fixture(scope="session")
def test_server(request: pytest.FixtureRequest, logger: logging.Logger) -> Generator[str, None, None]:
    """Fixture to run a simple HTTP server for serving the test HTML page."""
    logger.info("Starting test HTTP server")
    process = subprocess.Popen(["python", "-m", "http.server", "--directory", "data/test/"])
    time.sleep(3)
    yield "http://localhost:8000/"
    logger.info("Stopping test HTTP server")
    process.terminate()
    logger.info("Test HTTP server terminated")

@pytest.fixture(scope="module")
def playwright_browser(logger: logging.Logger, config: configparser.ConfigParser) -> Generator[Browser, None, None]:
    """Fixture to set up and tear down the Playwright browser instance."""
    try:
        logger.info("Launching Playwright browser...")
        playwright = sync_playwright().start()
        browser = playwright.webkit.launch_persistent_context(
                    user_data_dir=config.get("general", "user_data_path"),
                    headless=False)
        logger.info("Playwright browser launched successfully.")
        yield browser
        logger.info("Closing Playwright browser...")
        browser.close()
        logger.info("Playwright browser closed.")
    except Exception as e:
        logger.error(f"Failed to launch Playwright browser: {e}")
        raise

@pytest.fixture(scope="module")
def playwright_browser_no_data(logger: logging.Logger, config: configparser.ConfigParser) -> Generator[Browser, None, None]:
    """Fixture to set up and tear down the Playwright browser instance."""
    try:
        logger.info("Launching Playwright browser...")
        playwright = sync_playwright().start()
        browser = playwright.webkit.launch(
                    headless=False)
        context = browser.new_context()
        logger.info("Playwright browser launched successfully.")
        yield context
        logger.info("Closing Playwright browser...")
        browser.close()
        logger.info("Playwright browser closed.")
    except Exception as e:
        logger.error(f"Failed to launch Playwright browser: {e}")
        raise

@pytest.fixture(scope="module")
def playwright_page(playwright_browser: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down a Playwright page instance for tests."""
    page = playwright_browser.pages[0]
    logger.info("Navigating to test page...")
    page.goto("about:blank")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()

@pytest.fixture(scope="module")
def playwright_page_no_data(playwright_browser_no_data: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down a Playwright page instance for tests."""
    page = playwright_browser_no_data.new_page()
    logger.info("Navigating to test page...")
    page.goto("about:blank")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()

@pytest.fixture(scope="module")
def test_page(playwright_browser: Browser, logger: logging.Logger) -> Generator[Page, None, None]:
    """Fixture to set up and tear down the Playwright page instance."""
    page = playwright_browser.pages[0]
    logger.info("Navigating to test page...")
    page.goto("http://localhost:8000/selenium_test_page.html")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()

@pytest.fixture(scope="module")
def linkedin_facade(playwright_page: Page) -> Facade:
    """Provides a LinkedInFacade instance with a mocked Playwright Page with user data."""
    return Facade(playwright_page, LinkedInConstants)

@pytest.fixture(scope="module")
def linkedin_facade_no_data(playwright_page_no_data: Page) -> Facade:
    """Provides a LinkedInFacade instance with a mocked Playwright Page."""
    return Facade(playwright_page_no_data, LinkedInConstants)

@pytest.fixture(scope="module")
def test_job():
    return Job(
        title="Test Job", 
        company="Test Company", 
        location="Test Location", 
        url="about:blank",
        easy_apply=True
    )

@pytest.fixture(scope="module")
def credentials(config: configparser.ConfigParser) -> dict:
    """Provides LinkedIn credentials from the config."""
    return {
        "username": config.get("user_info", "username"),
        "password": config.get("user_info", "password"),
        "invalid_username": config.get("invalid_credentials", "username"),
        "invalid_password": config.get("invalid_credentials", "password")
    }