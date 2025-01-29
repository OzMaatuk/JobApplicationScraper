# tests\test_login.py

import configparser
import pytest
import src.logger as LOGGER
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.login.login import Login
from src.exceptions import LoginError
from src.constants.linkedin import LinkedInConstants
Locators = LinkedInConstants.Locators

logger = LOGGER.get(__name__)

class TestLogin:
    def test_successful_login(self, playwright_page_no_data: Page, config: configparser.ConfigParser) -> None:
        """Tests successful login using pytest-mock."""
        logger.info("Testing successful login scenario")

        username = config.get("user_info", "username")
        password = config.get("user_info", "password")

        login_manager = Login(playwright_page_no_data, LinkedInConstants)
        login_manager.login(username, password)

        assert playwright_page_no_data.url == LinkedInConstants.FEED_URL

    def test_login_timeout(self, mocker: pytest.MonkeyPatch, playwright_page_no_data: Page, config: configparser.ConfigParser) -> None:
        """Tests the timeout scenario during login."""
        logger.info("Testing login timeout scenario")

        mock_url_change = mocker.patch("src.login.login.wait_for_url_change", autospec=True)
        mock_url_change.side_effect = PlaywrightTimeoutError("Some test message.")

        username = config.get("user_info", "username")
        password = config.get("user_info", "password")

        login_manager = Login(playwright_page_no_data, LinkedInConstants)

        with pytest.raises(LoginError, match="Login failed Due to timeout."):
            login_manager.login(username, password)

    def test_login_unexpected_error(self, mocker: pytest.MonkeyPatch, playwright_page_no_data: Page, config: configparser.ConfigParser) -> None:
        """Tests for unexpected errors during login."""
        logger.info("Testing unexpected error scenario during login")

        mock_wait_element = mocker.patch("src.login.login.wait_for_element", autospec=True)
        mock_wait_element.side_effect = Exception("Test Unexpected Error")

        username = config.get("user_info", "username")
        password = config.get("user_info", "password")

        login_manager = Login(playwright_page_no_data, LinkedInConstants)

        with pytest.raises(LoginError, match=r"An unexpected error occurred during login: Test Unexpected Error"):
            login_manager.login(username, password)

    def test_invalid_credentials(self, playwright_page_no_data: Page, config: configparser.ConfigParser) -> None:
        """Tests the invalid credentials scenario during login."""
        logger.info("Testing invalid credentials scenario during login")

        invalid_username = config.get("invalid_credentials", "username")
        invalid_password = config.get("invalid_credentials", "password")

        login_manager = Login(playwright_page_no_data, LinkedInConstants)

        with pytest.raises(LoginError, match="Login failed Due to timeout."):
            login_manager.login(invalid_username, invalid_password)
