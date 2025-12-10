import logging
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


def wait_for_element_visible(page: Page, selector: str, timeout: int = 30000) -> Locator:
    locator = page.locator(selector)
    locator.wait_for(state="visible", timeout=timeout)
    logger.info(f"Element {selector} is visible")
    return locator


def wait_for_element_hidden(page: Page, selector: str, timeout: int = 30000):
    locator = page.locator(selector)
    locator.wait_for(state="hidden", timeout=timeout)
    logger.info(f"Element {selector} is hidden")


def wait_for_url_change(page: Page, expected_url: str, timeout: int = 30000):
    page.wait_for_url(f"**{expected_url}**", timeout=timeout)
    logger.info(f"URL changed to {expected_url}")


def take_screenshot(page: Page, filename: str):
    from pathlib import Path
    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{filename}.png"
    page.screenshot(path=str(screenshot_path))
    logger.info(f"Screenshot saved: {screenshot_path}")


def fill_form_field(page: Page, placeholder: str, value: str):
    page.get_by_placeholder(placeholder).fill(value)
    logger.info(f"Filled field '{placeholder}' with value")


def click_button_by_name(page: Page, button_name: str):
    page.get_by_role("button", name=button_name).click()
    logger.info(f"Clicked button: {button_name}")