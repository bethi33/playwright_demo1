"""Helper functions for automation testing"""
import logging
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


def wait_for_element_visible(page: Page, selector: str, timeout: int = 30000) -> Locator:
    """Wait for element to be visible"""
    locator = page.locator(selector)
    locator.wait_for(state="visible", timeout=timeout)
    logger.info(f"Element {selector} is visible")
    return locator


def wait_for_element_hidden(page: Page, selector: str, timeout: int = 30000):
    """Wait for element to be hidden"""
    locator = page.locator(selector)
    locator.wait_for(state="hidden", timeout=timeout)
    logger.info(f"Element {selector} is hidden")


def wait_for_url_change(page: Page, expected_url: str, timeout: int = 30000):
    """Wait for page URL to change to expected URL"""
    page.wait_for_url(f"**{expected_url}**", timeout=timeout)
    logger.info(f"URL changed to {expected_url}")


def take_screenshot(page: Page, filename: str):
    """Take a screenshot with custom filename"""
    from pathlib import Path
    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{filename}.png"
    page.screenshot(path=str(screenshot_path))
    logger.info(f"Screenshot saved: {screenshot_path}")


def fill_form_field(page: Page, placeholder: str, value: str):
    """Fill form field by placeholder text"""
    page.get_by_placeholder(placeholder).fill(value)
    logger.info(f"Filled field '{placeholder}' with value")


def click_button_by_name(page: Page, button_name: str):
    """Click button by button name"""
    page.get_by_role("button", name=button_name).click()
    logger.info(f"Clicked button: {button_name}")