import pytest
import logging
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base URL configuration
BASE_URL = "https://ecommerce-playground.lambdatest.io"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        logger.info("Browser launched")
        yield browser
        browser.close()
        logger.info("Browser closed")

@pytest.fixture
def context(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    logger.info("New browser context created")
    yield context
    context.close()
    logger.info("Browser context closed")

@pytest.fixture
def page(context):
    page = context.new_page()
    
    # Set default timeout to 30 seconds for all actions
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    logger.info("New page created")
    yield page
    
    # Capture screenshot on test failure
    if not page.is_closed():
        # Screenshot directory
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Get test name from request
        test_name = page.context.browser.contexts[0].__dict__.get('_name', 'unknown')
        screenshot_path = screenshot_dir / f"{test_name}.png"
        
        try:
            page.screenshot(path=str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
        
        page.close()
        logger.info("Page closed")

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def login_credentials():
    return {
        "valid_email": "sssdjsd@gmail.com",
        "valid_password": "123456",
        "invalid_email": "ssssdjddsd@gmail.com",
        "invalid_password": "wrongpass"
    }