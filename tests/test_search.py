# tests\test_search.py

import pytest
from configparser import ConfigParser
from playwright.sync_api import Page

from src.constants.linkedin import LinkedInConstants
import src.logger as LOGGER
from src.exceptions import SearchError
from src.search.linkedin.job_extractor import JobExtractor
from src.search.linkedin.search import LinkedInJobSearch
from src.models.job import Job

logger = LOGGER.get(__name__)


class TestLinkedInJobSearch:
    @pytest.fixture(autouse=True)
    def setup(self, playwright_page: Page, config: ConfigParser, mocker: pytest.MonkeyPatch):
        self.linkedin_page = playwright_page
        self.config = config
        self.mocker = mocker
        self.search = LinkedInJobSearch(playwright_page, LinkedInConstants)
        logger.info("Setup for LinkedInJobSearch tests")

    def test_build_search_url(self) -> None:
        """Tests the _build_search_url method."""
        logger.info("Starting test_build_search_url")
        keywords = self.config.get("search", "keywords", fallback="software engineer")
        location = self.config.get("search", "location", fallback="london")

        search_url = self.search._build_search_url(keywords, location)

        keywords = keywords.replace(' ', '+')
        location = location.replace(' ', '+')
        expected_url_part = f"keywords={keywords}&location={location}"

        assert expected_url_part in search_url
        logger.info("test_build_search_url completed successfully")

    def test_successful_search_mocked(self) -> None:
        """Tests a successful job search on LinkedIn with mocked extract_jobs method."""
        logger.info("Starting test_successful_search_mocked")
        keywords = self.config.get("search", "keywords", fallback="software engineer")
        location = self.config.get("search", "location", fallback="london")

        self.mocker.patch.object(self.linkedin_page, 'goto')
        self.mocker.patch.object(type(self.linkedin_page), 'url', new_callable=self.mocker.PropertyMock, return_value=f"https://www.linkedin.com/jobs/search?keywords={keywords.replace(' ', '+')}&location={location.replace(' ', '+')}")

        self.mocker.patch.object(JobExtractor, 'extract_jobs', return_value=[
            Job(title="Software Engineer", company="Tech Company", location="London", url="https://example.com", easy_apply=False)
        ])

        jobs = self.search.search_jobs(keywords=keywords, location=location)

        keywords = keywords.replace(' ', '+')
        location = location.replace(' ', '+')
        expected_url_part = f"keywords={keywords}&location={location}"

        assert expected_url_part in self.linkedin_page.url
        assert isinstance(jobs, list)
        assert len(jobs) > 0
        for job in jobs:
            assert isinstance(job, Job)
            assert job.title == "Software Engineer"
            assert job.company == "Tech Company"
            assert job.location == "London"
            assert job.url == "https://example.com"
        logger.info("test_successful_search_mocked completed successfully")

    def test_successful_search(self) -> None:
        """Tests a successful job search on LinkedIn with valid inputs."""
        logger.info("Starting test_successful_search")
        keywords = self.config.get("search", "keywords", fallback="software engineer")
        location = self.config.get("search", "location", fallback="london")
        epoch_ago = self.config.get("search", "epoch_ago", fallback="Past 24 hours")

        jobs = self.search.search_jobs(keywords=keywords, location=location, epoch_ago=epoch_ago, limit=4)

        keywords = keywords.replace(' ', '%20')
        location = location.replace(' ', '%20')
        expected_url_part = f"keywords={keywords}&location={location}"

        assert expected_url_part in self.linkedin_page.url
        assert isinstance(jobs, list)
        assert len(jobs) == 4
        for job in jobs:
            assert isinstance(job, Job)
            assert job.title
            assert job.company
            assert job.location
            assert job.url
        logger.info("test_successful_search completed successfully")

    def test_search_jobs_error(self) -> None:
        """Tests the LinkedInJobSearch.search_jobs method to handle SearchError."""
        logger.info("Starting test_search_jobs_error")
        keywords = self.config.get("search", "keywords", fallback="software engineer")
        location = self.config.get("search", "location", fallback="london")

        self.mocker.patch.object(LinkedInJobSearch, '_build_search_url', side_effect=Exception("Navigation error"))

        with pytest.raises(SearchError):
            self.search.search_jobs(keywords=keywords, location=location)
        
        logger.info("test_search_jobs_error completed successfully")

    def test_select_time_range(self) -> None:
        """Tests the _select_time_range method."""
        logger.info("Starting test_select_time_range")
        search_url = LinkedInConstants.JOBS_SEARCH_URL
        self.linkedin_page.goto(search_url)
        self.search._select_time_range()
        logger.info("test_select_time_range completed successfully")