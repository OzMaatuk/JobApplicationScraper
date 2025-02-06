# src/constants/indeed.py

from src.constants.constants import Constants

class IndeedConstants(Constants):

    # --- Indeed URLs ---
    LOGIN_URL = "https://secure.indeed.com/auth"
    FEED_URL = "https://www.indeed.com/"
    JOBS_SEARCH_URL = "https://il.indeed.com/"

    # --- Locators ---
    class Locators:
        class Login:
            USERNAME_FIELD = "input#login-email-input"
            PASSWORD_FIELD = "input#login-password-input"
            LOGIN_BUTTON = "button#login-submit-button"

        class Search:
            SEARCH_RESULTS = "//div[@id='mosaic-provider-jobcards']/ul"
            NUM_OF_SEARCH_RESULTS = "//div[contains(@class, 'jobsearch-JobCountAndSortPane-jobCount')]"

        class Job:
            TITLE = "//h2[@data-testid='simpler-jobTitle']"
            COMPANY = "//a[contains(@class, 'jobsearch-JobInfoHeader-companyNameLink')]"
            LOCATION = "//h2[@data-testid='jobsearch-JobInfoHeader-companyLocation']"
            URL = "//h2[contains(@class, 'jobTitle')]/a"
            DESCRIPTION = "//div[contains(@class, 'jobsearch-JobComponent-description')]"
            EASY_APPLY = "//span[@data-testid='indeedApply']"
            APPLY = "//button[contains(text(),'Apply Now')]"