# tests/test_facade.py

import src.logger as LOGGER
from pytest import raises
from configparser import ConfigParser
from src.linkedin.exceptions import LinkedInLoginError
from src.linkedin.facade import LinkedInFacade
from src.models.job import Job

logger = LOGGER.get(__name__)

# --- test linkedin facade login ---
def test_linkedin_facade_login(linkedin_facade: LinkedInFacade, config: ConfigParser) -> None:
    """
    Test the login functionality of LinkedInFacade.
    """
    logger.info("Testing LinkedInFacade.login() with valid credentials.")
    username = config.get("user_info", "username")
    password = config.get("user_info", "password")
    linkedin_facade.login(username, password)
    assert linkedin_facade.page.url == "https://www.linkedin.com/feed/"
    logger.debug("LinkedInFacade.login() executed successfully.")

def test_linkedin_facade_login_failure(linkedin_facade: LinkedInFacade, config: ConfigParser) -> None:
    """
    Test the login functionality of LinkedInFacade with invalid credentials.
    """
    logger.info("Testing LinkedInFacade.login() with invalid credentials.")
    username = config.get("invalid_credentials", "username")
    password = config.get("invalid_credentials", "password")
    with raises(LinkedInLoginError):
        linkedin_facade.login(username, password)
    logger.debug("LinkedInFacade.login() failed as expected with invalid credentials.")

# --- test linkedin facade search job ---
def test_linkedin_facade_search_jobs(
        mocker,
        linkedin_facade: LinkedInFacade,
        config: ConfigParser
    ) -> None:
    """Test the search_jobs functionality of LinkedInFacade."""
    # Mock the internal method _extract_job_information
    mock_extract_jobs_information = mocker.patch("src.linkedin.search.LinkedInJobSearch._extract_jobs_information")
    
    # Set up mock return value for _extract_job_information
    mock_extract_jobs_information.return_value = [
        Job(title="Software Engineer", company="Google", location="London", url="url1", description="Python Developer"),
        Job(title="Data Scientist", company="Amazon", location="New York", url="url2", description="Machine Learning Engineer")
    ]
    keywords = config.get("search", "keywords", fallback="NOT_FOUND")
    location = config.get("search", "location", fallback="NOT_FOUND")
    jobs = linkedin_facade.search_jobs(keywords, location)
    assert isinstance(jobs, list)
    assert len(jobs) == 2
    logger.info("test_linkedin_facade_search_jobs passed.")
    logger.debug(f"search_jobs returned {len(jobs)} jobs.")

def test_linkedin_facade_search_jobs_no_keywords(linkedin_facade: LinkedInFacade) -> None:
    """Tests search with no keywords."""
    with raises(ValueError):  # Assuming ValueError is raised for invalid search parameters
        linkedin_facade.search_jobs(keywords=None, location="London")
    logger.info("test_linkedin_facade_search_jobs_no_keywords passed.")

# --- test linkedin facade filter jobs ---
def test_linkedin_facade_filter_jobs(
    mocker,
    linkedin_facade: LinkedInFacade
) -> None:
    """Test the filter_jobs method of LinkedInFacade."""
    logger.info("Mocking DescriptionMatcher.matches method for filter_jobs test.")
    # Mock the matches method
    mocked_matched = mocker.patch("src.utils.description_matcher.DescriptionMatcher.matches")
    
    # Set up mock return value for matches
    mocked_matched.side_effect = lambda job_desc, user_desc: job_desc == user_desc

    jobs = [
        Job(title="Software Engineer", company="Google", location="London", url="url1", description="Python Developer"),
        Job(title="Data Scientist", company="Amazon", location="New York", url="url2", description="Machine Learning Engineer")
    ]
    logger.debug(f"Jobs before filtering: {jobs}")

    filtered_jobs = linkedin_facade.filter_jobs(jobs, "Python Developer")
    assert len(filtered_jobs) == 1, "filter_jobs should return one job."
    assert filtered_jobs[0].title == "Software Engineer", "Filtered job should be 'Software Engineer'."
    logger.debug("filter_jobs returned the correct filtered job.")