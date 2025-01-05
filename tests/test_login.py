# tests\test_login.py

import src.logger as LOGGER
import pytest
from src.login.login import LinkedInLogin
from src.linkedin.exceptions import LinkedInLoginError
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.constants import Locators

logger = LOGGER.get(__name__)

def test_successful_login(mocker: pytest.MonkeyPatch, playwright_page: Page, caplog: pytest.LogCaptureFixture) -> None:
    """Tests successful login using pytest-mock."""
    logger.info("Testing successful login scenario")

    mock_send_keys = mocker.patch("playwright_utils.send_keys_safely", autospec=True)
    mock_wait_element = mocker.patch("playwright_utils.wait_for_element", autospec=True, return_value=mocker.MagicMock(click=mocker.MagicMock()))
    mock_url_change = mocker.patch("playwright_utils.wait_for_url_change", autospec=True)

    login_manager = LinkedInLogin(playwright_page)
    login_manager.login("test_username", "test_password")

    mock_send_keys.assert_any_call(playwright_page, Locators.Login.USERNAME_FIELD, "test_username")
    mock_send_keys.assert_any_call(playwright_page, Locators.Login.PASSWORD_FIELD, "test_password")
    mock_wait_element.assert_called_once_with(playwright_page, Locators.Login.LOGIN_BUTTON)
    mock_wait_element.return_value.click.assert_called_once()
    mock_url_change.assert_called_once()

    assert "Testing successful login scenario" in caplog.text
    assert "Successful login test passed" in caplog.text

def test_login_timeout(mocker: pytest.MonkeyPatch, playwright_page: Page, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the timeout scenario during login."""
    logger.info("Testing login timeout scenario")

    mock_url_change = mocker.patch("playwright_utils.wait_for_url_change", autospec=True)
    mock_url_change.side_effect = PlaywrightTimeoutError("Simulated Timeout")

    login_manager = LinkedInLogin(playwright_page)

    with pytest.raises(LinkedInLoginError, match="Simulated Timeout"):
        login_manager.login("test_username", "test_password")

    assert "Testing login timeout scenario" in caplog.text
    assert "Timeout test passed" in caplog.text

def test_login_unexpected_error(mocker: pytest.MonkeyPatch, playwright_page: Page, caplog: pytest.LogCaptureFixture) -> None:
    """Tests for unexpected errors during login."""
    logger.info("Testing unexpected error scenario during login")

    mock_wait_element = mocker.patch("playwright_utils.wait_for_element", autospec=True)
    mock_wait_element.side_effect = Exception("Test Unexpected Error")

    login_manager = LinkedInLogin(playwright_page)

    with pytest.raises(LinkedInLoginError, match=r"An unexpected error occurred during login: Test Unexpected Error"):
        login_manager.login("test_username", "test_password")

    assert "Testing unexpected error scenario during login" in caplog.text
    assert "Unexpected error test passed" in caplog.text

def test_invalid_credentials(mocker: pytest.MonkeyPatch, playwright_page: Page, caplog: pytest.LogCaptureFixture) -> None:
    """Tests the invalid credentials scenario during login."""
    logger.info("Testing invalid credentials scenario during login")

    mock_send_keys = mocker.patch("playwright_utils.send_keys_safely", autospec=True)
    mock_wait_element = mocker.patch("playwright_utils.wait_for_element", autospec=True, return_value=mocker.MagicMock(click=mocker.MagicMock()))
    mock_url_change = mocker.patch("playwright_utils.wait_for_url_change", autospec=True)

    login_manager = LinkedInLogin(playwright_page)

    with pytest.raises(LinkedInLoginError, match="LinkedIn login failed."):
        login_manager.login("invalid_username", "invalid_password")

    assert "Testing invalid credentials scenario during login" in caplog.text
    assert "Invalid credentials test passed" in caplog.text