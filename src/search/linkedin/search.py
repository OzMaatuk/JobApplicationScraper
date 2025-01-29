# src\search\search.py
# TODO: add sleeps to avoid bot capture

from time import sleep
import src.logger as LOGGER
import urllib.parse
from typing import List, Dict, Optional
from playwright.sync_api import Page
from src.models.job import Job
from src.exceptions import SearchError
from src.search.linkedin.job_extractor import JobExtractor
from src.constants.constants import Constants


logger = LOGGER.get(__name__)


class JobSearch:
    """Manages job searching on LinkedIn."""

    def __init__(self, page: Page, constants: Constants) -> None:
        logger.debug("LinkedInJobSearch instance created")
        self.page = page
        self.constants = constants
        self.job_extractor = JobExtractor(page, constants)

    def search_jobs(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        epoch_ago: Optional[str] = None,
        additional_filters: Dict[str, str] = None,
        limit: Optional[int] = None,
    ) -> List[Job]:
        """Searches for jobs on LinkedIn."""
        try:
            logger.info(f"Searching for jobs with keywords '{keywords}' in '{location}'...")
            search_url = self._build_search_url(keywords, location, additional_filters)
            self.page.goto(search_url)
            self._select_time_range(epoch_ago)

            jobs = self.job_extractor.extract_jobs(None, limit)
            logger.info(f"Found {len(jobs)} jobs.")
            return jobs

        except Exception as e:
            error_msg = f"Failed to perform job search: {str(e)}"
            logger.error(error_msg)
            raise SearchError(error_msg) from e

    def _build_search_url(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        additional_filters: Optional[Dict[str, str]] = None,
    ) -> str:
        """Builds the LinkedIn search URL with the given parameters."""
        logger.debug(f"LinkedInJobSearch._build_search_url")

        base_url = self.constants.JOBS_SEARCH_URL + "?"
        url_parts = {}

        if keywords:
            url_parts["keywords"] = keywords
        if location:
            url_parts["location"] = location
        if additional_filters:
            # TODO: Implement proper filter handling
            raise NotImplementedError("Filter handling is not implemented yet.")

        return base_url + urllib.parse.urlencode(url_parts)
    
    def _select_time_range(self, epoch_ago: str = 86400) -> None:
        # TODO: improve code.
        if epoch_ago:
            self.page.locator("//button[text()='Date posted']").click()
            self.page.locator(f"//label[@for='timePostedRange-r{epoch_ago}']").click()
            self.page.get_by_role("button", name="Apply current filter to show").click()
            sleep(3)