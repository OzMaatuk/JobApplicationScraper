# tests\test_job_extractor.py

import pytest
from unittest.mock import MagicMock
from playwright.sync_api import Page
from src.search.job_extractor import JobExtractor
from src.models.job import Job

@pytest.fixture
def mock_page() -> Page:
    """Provides a mocked Playwright Page instance."""
    page = MagicMock(spec=Page)
    page.url = "https://www.linkedin.com/jobs/search/?distance=25&geoId=101620260&keywords=qa%20automation%20engineer"
    return page

@pytest.fixture
def job_extractor(mock_page: Page) -> JobExtractor:
    """Provides a JobExtractor instance with a mocked Page."""
    return JobExtractor(mock_page)

def test_simple_job_extractor(job_extractor: JobExtractor, mock_page: Page):
    mock_page.goto = MagicMock()
    mock_page.url = "https://www.linkedin.com/jobs/search/?distance=25&geoId=101620260&keywords=qa%20automation%20engineer"
    mock_page.locators = MagicMock()
    mock_page.locators.SEARCH_RESULTS = MagicMock(return_value=[MagicMock()] * 5)
    mock_page.locators.TITLE = MagicMock(return_value="Test Job")
    mock_page.locators.COMPANY = MagicMock(return_value="Test Company")
    mock_page.locators.LOCATION = MagicMock(return_value="Test Location")
    mock_page.locators.URL = MagicMock(return_value="about:blank")
    mock_page.locators.DESCRIPTION = MagicMock(return_value="Test Description")
    mock_page.locators.EASY_APPLY = MagicMock(return_value=True)
    mock_page.locators.APPLY = MagicMock(return_value=True)

    jobs = job_extractor.extract_jobs(limit=5)
    assert len(jobs) == 5
    for job in jobs:
        assert isinstance(job, Job)
        assert job.title == "Test Job"
        assert job.company == "Test Company"
        assert job.location == "Test Location"
        assert job.url == "about:blank"
        assert job.description == "Test Description"
        assert job.easy_apply is True

def test_long_job_extractor(job_extractor: JobExtractor, mock_page: Page):
    mock_page.goto = MagicMock()
    mock_page.url = "https://www.linkedin.com/jobs/search/?distance=25&geoId=101620260&keywords=qa%20automation%20engineer"
    mock_page.locators = MagicMock()
    mock_page.locators.SEARCH_RESULTS = MagicMock(return_value=[MagicMock()] * 48)
    mock_page.locators.TITLE = MagicMock(return_value="Test Job")
    mock_page.locators.COMPANY = MagicMock(return_value="Test Company")
    mock_page.locators.LOCATION = MagicMock(return_value="Test Location")
    mock_page.locators.URL = MagicMock(return_value="about:blank")
    mock_page.locators.DESCRIPTION = MagicMock(return_value="Test Description")
    mock_page.locators.EASY_APPLY = MagicMock(return_value=True)
    mock_page.locators.APPLY = MagicMock(return_value=True)

    jobs = job_extractor.extract_jobs(limit=48)
    assert len(jobs) == 48
    for job in jobs:
        assert isinstance(job, Job)
        assert job.title == "Test Job"
        assert job.company == "Test Company"
        assert job.location == "Test Location"
        assert job.url == "about:blank"
        assert job.description == "Test Description"
        assert job.easy_apply is True

@pytest.mark.skip(reason="no way of currently testing this")
def test_no_limit_job_extractor(job_extractor: JobExtractor, mock_page: Page):
    mock_page.goto = MagicMock()
    mock_page.url = "https://www.linkedin.com/jobs/search/?distance=25&geoId=101620260&keywords=qa%20automation%20engineer"
    mock_page.locators = MagicMock()
    mock_page.locators.SEARCH_RESULTS = MagicMock(return_value=[MagicMock()] * 10)
    mock_page.locators.TITLE = MagicMock(return_value="Test Job")
    mock_page.locators.COMPANY = MagicMock(return_value="Test Company")
    mock_page.locators.LOCATION = MagicMock(return_value="Test Location")
    mock_page.locators.URL = MagicMock(return_value="about:blank")
    mock_page.locators.DESCRIPTION = MagicMock(return_value="Test Description")
    mock_page.locators.EASY_APPLY = MagicMock(return_value=True)
    mock_page.locators.APPLY = MagicMock(return_value=True)
    mock_page.locators.NUM_OF_SEARCH_RESULTS = MagicMock(return_value="10")

    jobs = job_extractor.extract_jobs(limit=None)
    assert len(jobs) == 10
    for job in jobs:
        assert isinstance(job, Job)
        assert job.title == "Test Job"
        assert job.company == "Test Company"
        assert job.location == "Test Location"
        assert job.url == "about:blank"
        assert job.description == "Test Description"
        assert job.easy_apply is True