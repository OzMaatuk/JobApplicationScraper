# src\search\search.py

from time import sleep
import src.logger as LOGGER
import urllib.parse
from typing import Dict, Optional
from playwright.sync_api import Page
from src.search.indeed.job_extractor import JobExtractor
from src.constants.constants import Constants
from src.search.search import JobSearch


logger = LOGGER.get(__name__)


class IndeedJobSearch(JobSearch):
    """Manages job searching on Indeed."""

    def __init__(self, page: Page, constants: Constants) -> None:
        logger.debug("IndeedJobSearch instance created")
        super().__init__(page, constants)
        self.job_extractor = JobExtractor(page, constants)

    def _build_search_url(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        additional_filters: Optional[Dict[str, str]] = {"sort": "date", "fromage": "1"},
    ) -> str:
        """Builds the LinkedIn search URL with the given parameters."""
        logger.debug(f"LinkedInJobSearch._build_search_url")

        
        base_url = self.constants.JOBS_SEARCH_URL + "/jobs?"
        url_parts = {}

        if keywords:
            url_parts["q"] = keywords
        if location:
            url_parts["l"] = location
        if additional_filters:
            for filter in additional_filters:
                url_parts[filter] = additional_filters[filter]

        return base_url + urllib.parse.urlencode(url_parts)
    
    def _select_time_range(self, epoch_ago: str = 86400) -> None:
        pass