# src/linkedin/login.py

import src.logger as LOGGER
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.linkedin.exceptions import LinkedInLoginError
from playwright_utils import wait_for_element, wait_for_url_change, send_keys_safely
from src.constants import LINKEDIN_LOGIN_URL, LINKEDIN_FEED_URL, Locators

logger = LOGGER.get(__name__)

class LinkedInLogin:
    """Manages the login process for LinkedIn."""

    def __init__(self, page: Page):
        logger.debug("LinkedInLogin instance created")
        self.page = page

    def login(self, username: str, password: str):
        """Logs into LinkedIn."""
        logger.info("Starting LinkedIn login process...")
        linkedin_login_url = LINKEDIN_LOGIN_URL
        linkedin_feed_url = LINKEDIN_FEED_URL
        self.page.goto(linkedin_login_url)

        try:
            wait_for_url_change(self.page, linkedin_login_url)
            if linkedin_feed_url in self.page.url:
                logger.info("LinkedIn already login.")
            else:
                logger.info("LinkedIn not login, performing login.")
                send_keys_safely(self.page, Locators.Login.USERNAME_FIELD, username)
                send_keys_safely(self.page, Locators.Login.PASSWORD_FIELD, password)
                login_button = wait_for_element(self.page, Locators.Login.LOGIN_BUTTON)
                login_button.click()
                wait_for_url_change(self.page, linkedin_feed_url)
                if linkedin_feed_url in self.page.url:
                    logger.info("LinkedIn login successful.")
                else:
                    raise LinkedInLoginError("LinkedIn login failed.")
        except PlaywrightTimeoutError:
            if linkedin_feed_url in self.page.url:
                logger.info("LinkedIn already login.")
            else:
                raise LinkedInLoginError("LinkedIn login failed Due to timeout.")
        except Exception as e:
            raise LinkedInLoginError(f"An unexpected error occurred during login: {str(e)}")