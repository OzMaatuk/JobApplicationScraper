# src\search\search.py
# TODO: add sleeps to avoid bot capture

from abc import ABC, abstractmethod
from time import sleep
import src.logger as LOGGER
from typing import List, Dict, Optional
from playwright.sync_api import Page
from src.models.job import Job
from src.exceptions import SearchError
from src.constants.constants import Constants


logger = LOGGER.get(__name__)


class JobSearch(ABC):
    """Manages job searching on LinkedIn."""

    def __init__(self, page: Page, constants: Constants) -> None:
        logger.debug("LinkedInJobSearch instance created")
        self.page = page
        self.constants = constants

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

    @abstractmethod
    def _build_search_url(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        additional_filters: Optional[Dict[str, str]] = None,
    ) -> str:
        """Builds the LinkedIn search URL with the given parameters."""
        raise NotImplementedError("Method not implemented")
        
    @abstractmethod
    def _select_time_range(self, epoch_ago: str = 86400) -> None:
        raise NotImplementedError("Method not implemented")
        