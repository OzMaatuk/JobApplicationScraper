# src/linkedin/facade.py

import src.logger as LOGGER
from typing import List, Dict, Optional
from playwright.sync_api import Page

from src.login.login import LinkedInLogin
from src.search.search import LinkedInJobSearch
from src.models.job import Job
from src.utils.description_matcher import DescriptionMatcher
from src.constants import LINKEDIN_FEED_URL, DEFAULT_FUZZ_THRESHOLD


logger = LOGGER.get(__name__)

class LinkedInFacade:
    """Facade class for LinkedIn automation."""

    def __init__(self, page: Page, method: str = "fuzz", threshold: int = DEFAULT_FUZZ_THRESHOLD):
        logger.debug("LinkedInFacade instance is created")
        self.page = page
        self.linkedin_login = LinkedInLogin(self.page)
        self.linkedin_search = LinkedInJobSearch(self.page)
        self.matcher = DescriptionMatcher(method, threshold)

    def login(self, username: str, password: str) -> None:
        logger.debug("LinkedInFacade.login")
        if self.page.url != LINKEDIN_FEED_URL:
            self.linkedin_login.login(username, password)

    def search_jobs(self, 
                    keywords: Optional[str] = None, 
                    location: Optional[str] = None, 
                    geold: Optional[str] = None, 
                    filters: Optional[Dict[str, str]] = None,
                    limit: Optional[int] = None
                ) -> List[Job]:
        logger.debug("LinkedInFacade.search_jobs")
        return self.linkedin_search.search_jobs(keywords, location, geold, filters, limit)
    

    def filter_jobs(self, jobs: List[Job], user_description: str) -> List[Job]:
        """Filters jobs based on user description."""
        logger.debug("LinkedInFacade.filter_jobs")
        jobs_to_apply = [job for job in jobs if self.matcher.matches(job.description, user_description)]
        return jobs_to_apply