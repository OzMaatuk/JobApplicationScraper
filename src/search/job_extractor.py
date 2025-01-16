# src\search\job_extractor.py


import re
from time import sleep
import src.logger as LOGGER
from typing import Optional, List, Dict
from playwright.sync_api import Page, Locator

from src.models.job import Job
from playwright_utils import (
    get_element_attribute,
    get_element_text,
    wait_for_all_elements,
    wait_for_element,
    wait_for_url_change,
)
from src.constants import URL_PAGE_NUM_PARAMETER, Locators, NUM_OF_JOBS_IN_PAGE


logger = LOGGER.get(__name__)



class JobExtractor:
    
    @property
    def search_results_elements(self) -> List[Locator]:
        return wait_for_all_elements(self.page, self.locators.SEARCH_RESULTS)

    @property
    def job_title(self) -> Optional[str]:
        return get_element_text(self.page, self.locators.TITLE)

    @property
    def job_company(self) -> Optional[str]:
        return get_element_text(self.page, self.locators.COMPANY)

    @property
    def job_location(self) -> Optional[str]:
        return get_element_text(self.page, self.locators.LOCATION)

    @property
    def job_url(self) -> Optional[str]:
        return get_element_attribute(self.page, self.locators.URL, "href")

    @property
    def job_description(self) -> Optional[str]:
        return get_element_text(self.page, self.locators.DESCRIPTION)

    @property
    def is_job_easy_apply(self) -> bool:
        try:
            wait_for_element(self.page, self.locators.EASY_APPLY)
            return True
        except Exception:
            return False
    
    @property
    def is_job_apply_button(self) -> bool:
        try:
            wait_for_element(self.page, self.locators.APPLY)
            return True
        except Exception:
            return False


    def __init__(self, page: Page):
        logger.debug("JobExtractor instance created")
        self.page = page
        self.locators = Locators.Job
    
    def _next_results_page(self) -> None:
        """Navigate to the next page in the search results"""
        logger.debug("JobExtractor._next_results_page")
        current_url = self.page.url

        if URL_PAGE_NUM_PARAMETER in current_url:
            pattern = fr"{URL_PAGE_NUM_PARAMETER}(\d+)"
            match = re.search(pattern, current_url)
            if match:
                current_start_str = match.group(1)
                new_start = int(current_start_str) + NUM_OF_JOBS_IN_PAGE
                updated_url = re.sub(pattern, f"&start={new_start}", current_url)
                self.page.goto(updated_url)
            else:
                raise ValueError("Could not find 'start' parameter in the URL.")
        else:
            self.page.goto(f"{self.page.url}{URL_PAGE_NUM_PARAMETER}{NUM_OF_JOBS_IN_PAGE}")

    def extract_jobs(
        self, url: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Job]:
        """Extracts job information from the search results page."""
        logger.debug("JobExtractor.extract_jobs")

        logger.info("Extracting job information from search results.")
        jobs = []

        if url:
            self.page.goto(url)
            wait_for_url_change(self.page, url)
        try:
            jobs = self._process_job_elements(limit)
        except Exception as e:
            logger.error(f"Failed to extract jobs: {str(e)}")

        logger.info(f"Extracted {len(jobs)} jobs in total.")
        return jobs

    def _process_job_elements(self, limit: Optional[int] = None) -> List[Job]:
        """Process job elements from search results, extracting and validating job data."""
        logger.debug("JobExtractor._process_job_elements")
        
        limit = self._determine_job_limit(limit)
        jobs = []
        processed_count = 0
        elements = self.search_results_elements

        while processed_count < limit:
            try:
                
                if processed_count >= len(elements):
                    processed_count = 0
                    limit -= len(elements)
                    self._next_results_page()
                    elements.append(self.search_results_elements)
                
                element = elements[processed_count]                
                element.click()
                
                job = self._process_single_job_element()
                if job: jobs.append(job)

                processed_count += 1
            except Exception as e:
                logger.warning(f"Failed processing job elements: {str(e)}")
                continue

        return jobs

    def _determine_job_limit(self, limit: Optional[int]) -> int:
        """Determine the number of jobs to process."""
        logger.debug("JobExtractor._determine_job_limit")
        if limit is not None:
            return limit
        
        limit_text = get_element_text(self.page, self.locators.NUM_OF_SEARCH_RESULTS)
        match = re.match(r"^\d+", limit_text)
        
        if match:
            return int(match.group(0))
        
        raise ValueError("Cannot determine the total number of search results")

    def _process_single_job_element(self) -> Optional[Job]:
        """Process a single job element, extracting and validating its data."""
        logger.debug("JobExtractor._process_single_job_element")
        job_data = self._extract_single_job_data()

        if ((not job_data['easy_apply']) and (not self.is_job_apply_button)):
            logger.info(f"Already applied to job: {job_data['title']}")
            return None

        if self._is_valid_job_data(job_data):
            job = self._create_job_object(job_data)
            logger.info(f"Job added: {job_data['title']}")
            return job
        
        self._log_invalid_job_data(job_data)
        return None

    def _extract_single_job_data(self) -> Dict:
        logger.debug("JobExtractor._extract_single_job_data")
        job = {
            "title": self.job_title,
            "company": self.job_company,
            "location": self.job_location,
            "url": self.job_url,
            "description": self.job_description,
            "easy_apply": self.is_job_easy_apply,
        }
        logger.debug(f"extracted job details: {job}")
        return job

    def _is_valid_job_data(self, job_data: Dict) -> bool:
        logger.debug("JobExtractor._is_valid_job_data")
        required_fields = ["title", "company", "location", "url"]
        return all(job_data.get(field) for field in required_fields)

    def _create_job_object(self, job_data: Dict) -> Job:
        logger.debug("JobExtractor._create_job_object")
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            url=job_data["url"],
            description=job_data["description"],
            easy_apply=job_data["easy_apply"],
        )
        logger.debug(f"Created job object: {job}")
        return job

    def _log_invalid_job_data(self, job_data: Dict) -> None:
        logger.debug("JobExtractor._log_invalid_job_data")
        logger.warning(
            "Missing information for a job element. Skipping. "
            f"Data found: title={job_data['title']}, "
            f"company={job_data['company']}, "
            f"location={job_data['location']}, "
            f"url={job_data['url']}"
        )