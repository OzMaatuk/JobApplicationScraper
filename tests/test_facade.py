# tests/test_facade.py

import src.logger as LOGGER
from pytest import raises
from configparser import ConfigParser
from src.exceptions import LoginError
from src.facade import Facade
from src.models.job import Job

logger = LOGGER.get(__name__)

class TestLinkedInFacade:
    # --- test linkedin facade login ---
    def test_linkedin_facade_login(self, linkedin_facade_no_data: Facade, config: ConfigParser) -> None:
        """
        Test the login functionality of Facade.
        """
        logger.info("Testing Facade.login() with valid credentials.")
        username = config.get("user_info", "username")
        password = config.get("user_info", "password")
        linkedin_facade_no_data.login(username, password)
        assert linkedin_facade_no_data.page.url == "https://www.linkedin.com/feed/"
        logger.debug("Facade.login() executed successfully.")

    def test_linkedin_facade_login_failure(self, linkedin_facade_no_data: Facade, config: ConfigParser) -> None:
        """
        Test the login functionality of Facade with invalid credentials.
        """
        logger.info("Testing Facade.login() with invalid credentials.")
        username = config.get("invalid_credentials", "username")
        password = config.get("invalid_credentials", "password")
        with raises(LoginError):
            linkedin_facade_no_data.login(username, password)
        logger.debug("Facade.login() failed as expected with invalid credentials.")

    # --- test linkedin facade search job ---
    def test_linkedin_facade_search_jobs(
            self,
            mocker,
            linkedin_facade: Facade,
            config: ConfigParser
        ) -> None:
        """Test the search_jobs functionality of Facade."""
        # Mock the internal method _extract_job_information
        mock_extract_jobs = mocker.patch("src.search.search.JobExtractor.extract_jobs")
        
        # Set up mock return value for _extract_job_information
        mock_extract_jobs.return_value = [
            Job(title="Software Engineer", company="Google", location="London", url="url1", description="Python Developer", easy_apply=False),
            Job(title="Data Scientist", company="Amazon", location="New York", url="url2", description="Machine Learning Engineer", easy_apply=True)
        ]
        keywords = config.get("search", "keywords", fallback="NOT_FOUND")
        location = config.get("search", "location", fallback="NOT_FOUND")
        jobs = linkedin_facade.search_jobs(keywords=keywords, location=location, limit=2)
        assert isinstance(jobs, list)
        assert len(jobs) == 2
        logger.info("test_linkedin_facade_search_jobs passed.")
        logger.debug(f"search_jobs returned {len(jobs)} jobs.")

    def test_linkedin_facade_search_jobs_no_keywords(self, mocker, linkedin_facade: Facade) -> None:
        """Tests search with no keywords."""
        logger.info("Testing search_jobs with no keywords.")
        
        # Mock the internal method _extract_job_information
        mock_extract_jobs = mocker.patch("src.search.search.JobExtractor.extract_jobs")
        
        # Set up mock return value for _extract_job_information
        mock_extract_jobs.return_value = [
            Job(title="Software Engineer", company="Google", location="London", url="url1", description="Python Developer", easy_apply=False),
            Job(title="Data Scientist", company="Amazon", location="New York", url="url2", description="Machine Learning Engineer", easy_apply=True)
        ]
        jobs = linkedin_facade.search_jobs(keywords=None, location=None, limit=2)
        assert isinstance(jobs, list)
        assert len(jobs) == 2
        logger.info("test_linkedin_facade_search_jobs_no_keywords passed.")
        logger.debug(f"search_jobs returned {len(jobs)} jobs.")

    # --- test linkedin facade filter jobs ---
    def test_linkedin_facade_filter_jobs(
        self,
        mocker,
        linkedin_facade: Facade
    ) -> None:
        """Test the filter_jobs method of Facade."""
        logger.info("Mocking DescriptionMatcher.matches method for filter_jobs test.")
        # Mock the matches method
        mocked_matched = mocker.patch("src.utils.description_matcher.DescriptionMatcher.matches")
        
        # Set up mock return value for matches
        mocked_matched.side_effect = lambda job_desc, user_desc: job_desc == user_desc

        jobs = [
            Job(title="Software Engineer", company="Google", location="London", url="url1", description="Python Developer", easy_apply=False),
            Job(title="Data Scientist", company="Amazon", location="New York", url="url2", description="Machine Learning Engineer", easy_apply=True)
        ]
        logger.debug(f"Jobs before filtering: {jobs}")

        filtered_jobs = linkedin_facade.filter_jobs(jobs, "Python Developer")
        assert len(filtered_jobs) == 1, "filter_jobs should return one job."
        assert filtered_jobs[0].title == "Software Engineer", "Filtered job should be 'Software Engineer'."
        logger.debug("filter_jobs returned the correct filtered job.")