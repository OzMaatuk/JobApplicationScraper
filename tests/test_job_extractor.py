# tests\test_job_extractor.py

import pytest
from playwright.sync_api import Page

import src.logger as LOGGER
from src.constants.constants import Constants
from src.search.linkedin.job_extractor import JobExtractor
from src.models.job import Job
from src.constants.constants import Constants

logger = LOGGER.get(__name__)


class TestJobExtractor:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: pytest.MonkeyPatch):
        self.mocker = mocker
        self.mock_page = self.mocker.MagicMock(spec=Page)
        self.job_extractor = JobExtractor(self.mock_page, Constants)
        logger.info("Setup for JobExtractor tests")

    def test_extract_job_information_no_results(self) -> None:
        """Tests the extraction of job information when no results are found."""
        logger.info("Starting test_extract_job_information_no_results")

        self.mocker.patch.object(JobExtractor, 'search_results_elements', return_value=[])

        jobs = self.job_extractor.extract_jobs(Constants.JOBS_SEARCH_URL, 4)

        assert isinstance(jobs, list)
        assert len(jobs) == 0
        logger.info("test_extract_job_information_no_results completed successfully")

    def test_extract_job_information(self) -> None:
        """Tests the extraction of job information from a real LinkedIn search results page."""
        logger.info("Starting test_extract_job_information")

        self.mocker.patch.object(JobExtractor, 'search_results_elements', [
            self.mocker.MagicMock(), self.mocker.MagicMock(), self.mocker.MagicMock(), self.mocker.MagicMock()
        ])
        self.mocker.patch.object(JobExtractor, 'job_title', new_callable=self.mocker.PropertyMock, return_value="Software Engineer")
        self.mocker.patch.object(JobExtractor, 'job_company', new_callable=self.mocker.PropertyMock, return_value="Tech Company")
        self.mocker.patch.object(JobExtractor, 'job_location', new_callable=self.mocker.PropertyMock, return_value="San Francisco")
        self.mocker.patch.object(JobExtractor, 'job_url', new_callable=self.mocker.PropertyMock, return_value="https://example.com")
        self.mocker.patch.object(JobExtractor, 'job_description', new_callable=self.mocker.PropertyMock, return_value="Job description")
        self.mocker.patch.object(JobExtractor, 'is_job_easy_apply', new_callable=self.mocker.PropertyMock, return_value=True)
        self.mocker.patch.object(JobExtractor, 'is_job_apply_button', new_callable=self.mocker.PropertyMock, return_value=True)

        jobs = self.job_extractor.extract_jobs(Constants.JOBS_SEARCH_URL, 4)

        assert isinstance(jobs, list)
        assert len(jobs) == 4
        for job in jobs:
            assert isinstance(job, Job)
            assert job.title == "Software Engineer"
            assert job.company == "Tech Company"
            assert job.location == "San Francisco"
            assert job.url == "https://example.com"
            assert job.description == "Job description"
            assert job.easy_apply is True
        logger.info("test_extract_job_information completed successfully")