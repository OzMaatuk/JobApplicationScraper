# src\search\search.py

import src.logger as LOGGER
import urllib.parse
from typing import List, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.models.job import Job
from playwright_utils import wait_for_url_change
from src.linkedin.exceptions import LinkedInSearchError
from src.search.job_extractor import JobExtractor
from src.constants import LINKEDIN_JOBS_SEARCH_URL


logger = LOGGER.get(__name__)


class LinkedInJobSearch:
    """Manages job searching on LinkedIn."""

    def __init__(self, page: Page):
        logger.debug("LinkedInJobSearch instance created")
        self.page = page
        self.job_extractor = JobExtractor(page)

    def search_jobs(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        geold: Optional[str] = None,
        additional_filters: Dict[str, str] = None,
        limit: Optional[int] = None,
    ) -> List[Job]:
        """Searches for jobs on LinkedIn."""
        try:
            logger.info(f"Searching for jobs with keywords '{keywords}' in '{location}' in {geold}'...")
            search_url = self._build_search_url(keywords, location, geold, additional_filters)
            self._navigate_to_search(search_url)

            jobs = self.job_extractor.extract_jobs(None, limit)
            logger.info(f"Found {len(jobs)} jobs.")
            return jobs

        except Exception as e:
            error_msg = f"Failed to perform job search: {str(e)}"
            logger.error(error_msg)
            raise LinkedInSearchError(error_msg) from e

    def _build_search_url(
        self,
        keywords: Optional[str],
        location: Optional[str],
        geold: Optional[str],
        additional_filters: Optional[Dict[str, str]],
    ) -> str:
        """Builds the LinkedIn search URL with the given parameters."""
        logger.debug(f"LinkedInJobSearch._build_search_url")

        base_url = LINKEDIN_JOBS_SEARCH_URL
        url_parts = {}

        if keywords:
            url_parts["keywords"] = keywords
        if location:
            url_parts["location"] = location
        if geold:
            url_parts["geold"] = geold
        if additional_filters:
            # TODO: Implement proper filter handling
            raise NotImplementedError("Filter handling is not implemented yet.")

        return base_url + urllib.parse.urlencode(url_parts)

    def _navigate_to_search(self, search_url: str) -> None:
        """Navigates to the search URL and waits for the page to load."""
        logger.debug(f"LinkedInJobSearch._navigate_to_search")

        current_url = self.page.url
        self.page.goto(search_url)

        try:
            wait_for_url_change(self.page, current_url)
        except PlaywrightTimeoutError:
            logger.warning(
                "Search URL did not change, but results might have been updated. Check Search Results"
            )
