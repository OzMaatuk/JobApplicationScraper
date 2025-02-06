# src\search\search.py

from time import sleep
import src.logger as LOGGER
import urllib.parse
from typing import Dict, Optional
from playwright.sync_api import Page
from src.search.linkedin.job_extractor import JobExtractor
from src.constants.constants import Constants
from src.search.search import JobSearch


logger = LOGGER.get(__name__)


class LinkedInJobSearch(JobSearch):
    """Manages job searching on LinkedIn."""

    def __init__(self, page: Page, constants: Constants) -> None:
        logger.debug("LinkedInJobSearch instance created")
        super().__init__(page, constants)
        self.job_extractor = JobExtractor(page, constants)

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