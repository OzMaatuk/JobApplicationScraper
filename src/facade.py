# src/facade.py

import src.logger as LOGGER
from playwright.sync_api import Page
from typing import List, Dict, Optional

from src.login.login import Login
from src.search.linkedin.search import LinkedInJobSearch
from src.search.indeed.search import IndeedJobSearch
from src.models.job import Job
from src.utils.description_matcher import DescriptionMatcher

from src.constants.constants import Constants


logger = LOGGER.get(__name__)

class Facade:
    """Facade class for job search automation."""

    def __init__(self, page: Page, constants: Constants, site_type: str, method: str = "llm", threshold: int = Constants.DEFAULT_THRESHOLD):
        logger.debug("Facade instance is created")
        self.page = page
        self.login_obj = Login(self.page, constants)
        self.matcher = DescriptionMatcher(method, threshold)
        self.constants = constants

        if site_type == "linkedin":
            self.search_obj = LinkedInJobSearch(self.page, constants)
        elif site_type == "indeed":
            self.search_obj = IndeedJobSearch(self.page, constants)
        else:
            raise ValueError(f"Unsupported site type: {site_type}")

    def login(self, username: str, password: str) -> None:
        logger.debug("Facade.login")
        if self.page.url != self.constants.FEED_URL:
            self.login_obj.login(username, password)

    def search_jobs(self, 
                    keywords: Optional[str] = None, 
                    location: Optional[str] = None,
                    epoch_ago: Optional[str] = None,
                    filters: Optional[Dict[str, str]] = None,
                    limit: Optional[int] = None
                ) -> List[Job]:
        logger.debug("Facade.search_jobs")
        return self.search_obj.search_jobs(keywords=keywords, 
                                           location=location, 
                                           epoch_ago=epoch_ago, 
                                           additional_filters=filters, 
                                           limit=limit)
    
    def filter_jobs(self, jobs: List[Job], user_description: str) -> List[Job]:
        """Filters jobs based on user description."""
        logger.debug("Facade.filter_jobs")
        jobs_to_apply = [job for job in jobs if self.matcher.matches(job.description, user_description)]
        return jobs_to_apply