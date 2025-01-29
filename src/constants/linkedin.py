# src/constants/linkedin.py

from src.constants.constants import Constants

class LinkedInConstants(Constants):

    # --- LinkedIn URLs ---
    LOGIN_URL = "https://www.linkedin.com/login"
    FEED_URL = "https://www.linkedin.com/feed/"
    JOBS_SEARCH_URL = "https://www.linkedin.com/jobs/search/"

    # --- Locators ---
    class Locators:
        class Login:
            USERNAME_FIELD = "input#username"
            PASSWORD_FIELD = "input#password"
            LOGIN_BUTTON = "button[data-litms-control-urn='login-submit']"

        class Search:
            SEARCH_RESULTS = "//li[contains(@class, 'occludable-update')]"
            JOBS_SEARCH_KEYWORDS = "input[name='keywords']"
            JOBS_SEARCH_LOCATION = "input[name='location']"
            NUM_OF_SEARCH_RESULTS = "//*[@id=\"main\"]/div/div[2]/div[1]/header/div[1]/small"

        class Job:
            TITLE = "//a[@class='ember-view']"
            COMPANY = "xpath=//div[contains(@class, 'company-name')]"
            LOCATION = "xpath=//div[contains(@class, 'primary-description')]"
            URL = "//a[@class='ember-view']"
            DESCRIPTION = "//div[@id='job-details']"
            EASY_APPLY = "//button[span[text()='Easy Apply']]"
            APPLY = "//button[span[text()='Apply']]"
            SEARCH_RESULTS = "//li[contains(@class, 'occludable-update')]"

    NUM_OF_JOBS_IN_PAGE = 25
    URL_PAGE_NUM_PARAMETER = "&start="

    # --- Easy Apply Form Constants ---
    class EasyApplyForm:
        NEXT_BUTTON = '//button[contains(text(), "Next")]'
        SUBMIT_BUTTON = '//button[@type="submit" or contains(text(), "Submit")]'
        RADIO_BUTTON_LABEL = "./following-sibling::*[contains(concat(' ',normalize-space(@class),' '),' fb-radio-button__label ')]"
