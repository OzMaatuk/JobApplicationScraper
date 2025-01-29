# src/login/login.py

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from playwright_utils import wait_for_element, wait_for_url_change, send_keys_safely
import src.logger as LOGGER
from src.exceptions import LoginError
from src.constants.constants import Constants

logger = LOGGER.get(__name__)

class Login:
    """Manages the login process for LinkedIn."""

    def __init__(self, page: Page, constants: Constants):
        logger.debug("Login instance created")
        self.page = page
        self.constants = constants

    def login(self, username: str, password: str):
        """Logs into site."""
        logger.info("Starting Login process...")
        login_url = self.constants.LOGIN_URL
        feed_url = self.constants.FEED_URL
        self.page.goto(login_url)

        try:
            wait_for_url_change(self.page, login_url)
            if feed_url in self.page.url:
                logger.info("Already login.")
            else:
                logger.info("Not login, performing login.")
                send_keys_safely(self.page, self.constants.Locators.Login.USERNAME_FIELD, username)
                send_keys_safely(self.page, self.constants.Locators.Login.PASSWORD_FIELD, password)
                login_button = wait_for_element(self.page, self.constants.Locators.Login.LOGIN_BUTTON)
                login_button.click()
                wait_for_url_change(self.page, feed_url)
                if feed_url in self.page.url:
                    logger.info("Login successful.")
                else:
                    raise LoginError("Login failed.")
        except PlaywrightTimeoutError:
            if feed_url in self.page.url:
                logger.info("Already login.")
            else:
                raise LoginError("Login failed Due to timeout.")
        except Exception as e:
            raise LoginError(f"An unexpected error occurred during login: {str(e)}")