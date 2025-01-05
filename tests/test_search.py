# tests\test_search.py

import pytest
from configparser import ConfigParser
from playwright.sync_api import Page

import src.logger as LOGGER
from src.linkedin.exceptions import LinkedInSearchError
from src.search.search import LinkedInJobSearch
from src.models.job import Job

logger = LOGGER.get(__name__)

def test_successful_search(playwright_page: Page, config: ConfigParser, mocker: pytest.MonkeyPatch) -> None:
    """Tests a successful job search on LinkedIn with valid inputs."""
    logger.info("Starting test_successful_search")
    keywords = config.get("search", "keywords", fallback="software engineer")
    location = config.get("search", "location", fallback="london")
    geold = config.get("search", "geold", fallback="")

    mock_goto = mocker.patch.object(playwright_page, "goto")
    search = LinkedInJobSearch(playwright_page)
    search.search_jobs(keywords, location, geold)

    keywords = keywords.replace(' ', '+')
    location = location.replace(' ', '+')
    expected_url_part = f"keywords={keywords}&location={location}&geold={geold}"

    mock_goto.assert_called_once()
    assert expected_url_part in mock_goto.call_args[0][0]
    logger.info("test_successful_search completed successfully")

def test_failed_search_invalid_input(playwright_page: Page) -> None:
    """Tests that a SearchError is raised when invalid input is provided."""
    logger.info("Starting test_failed_search_invalid_input")
    invalid_keywords = ""
    valid_location = "London"
    with pytest.raises(LinkedInSearchError, match="Failed to perform job search"):
        LinkedInJobSearch(playwright_page).search_jobs(invalid_keywords, valid_location)
    logger.info("test_failed_search_invalid_input completed successfully")

def test_search_with_additional_filters(playwright_page: Page, config: ConfigParser, mocker: pytest.MonkeyPatch) -> None:
    """Tests job search functionality with additional filters."""
    logger.info("Starting test_search_with_additional_filters")
    keywords = config.get("search", "keywords", fallback="software engineer")
    location = config.get("search", "location", fallback="london")
    geold = config.get("search", "geold", fallback="")
    additional_filters = {"f_WT": "2", "f_E": "2"}

    mock_goto = mocker.patch.object(playwright_page, "goto")
    search = LinkedInJobSearch(playwright_page)
    search.search_jobs(keywords, location, geold, additional_filters)

    keywords = keywords.replace(' ', '+')
    location = location.replace(' ', '+')
    expected_url_part = f"keywords={keywords}&location={location}&geold={geold}&f_WT=2&f_E=2"

    mock_goto.assert_called_once()
    assert expected_url_part in mock_goto.call_args[0][0]
    logger.info("test_search_with_additional_filters completed successfully")

def test_extract_job_information_with_real_page(playwright_page: Page, mocker: pytest.MonkeyPatch) -> None:
    """Tests the extraction of job information from a real LinkedIn search results page."""
    logger.info("Starting test_extract_job_information_with_real_page")
    search_url = "https://www.linkedin.com/jobs/search/"
    mocker.patch.object(playwright_page, "goto", return_value=None)
    mocker.patch.object(playwright_page, "query_selector_all", return_value=[
        mocker.MagicMock(inner_text="Job Title\nCompany\nLocation\nhttps://example.com")
    ])

    search = LinkedInJobSearch(playwright_page)
    jobs = search.job_extractor.extract_jobs(None, 4)

    assert isinstance(jobs, list)
    assert len(jobs) > 0
    for job in jobs:
        assert isinstance(job, Job)
        assert job.title is not None
        assert job.company is not None
        assert job.location is not None
        assert job.url is not None
    logger.info("test_extract_job_information_with_real_page completed successfully")

def test_extract_job_information_no_results(playwright_page: Page, mocker: pytest.MonkeyPatch) -> None:
    """Tests the extraction of job information when no results are found."""
    logger.info("Starting test_extract_job_information_no_results")

    mocker.patch.object(playwright_page, "query_selector_all", return_value=[])

    search = LinkedInJobSearch(playwright_page)
    jobs = search.job_extractor.extract_jobs(None, 4)

    assert isinstance(jobs, list)
    assert len(jobs) == 0
    logger.info("test_extract_job_information_no_results completed successfully")

def test_extract_job_information_missing_info(playwright_page: Page, mocker: pytest.MonkeyPatch) -> None:
    """Tests missing title, company, location, or url."""
    logger.info("Starting test_extract_job_information_missing_info")

    mocker.patch.object(playwright_page, "query_selector_all", return_value=[
        mocker.MagicMock(inner_text="\nCompany\nLocation\nhttps://example.com")
    ])

    search = LinkedInJobSearch(playwright_page)
    jobs = search.job_extractor.extract_jobs(None, 4)

    assert len(jobs) == 0  # No jobs should be returned as title is missing
    logger.info("test_extract_job_information_missing_info completed successfully")

# Additional test cases can be added as needed.