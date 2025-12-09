"""Test configuration and constants for automation testing"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URLs
BASE_URL = os.getenv("BASE_URL", "https://ecommerce-playground.lambdatest.io")
LOGIN_URL = f"{BASE_URL}/index.php?route=account/login"
HOME_URL = f"{BASE_URL}/index.php?route=common/home"
REGISTER_URL = f"{BASE_URL}/index.php?route=account/register"

# Test Credentials
VALID_EMAIL = os.getenv("VALID_EMAIL", "sssdjsd@gmail.com")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "123456")
INVALID_EMAIL = os.getenv("INVALID_EMAIL", "ssssdjddsd@gmail.com")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD", "wrongpass")

# Timeouts (in milliseconds)
DEFAULT_TIMEOUT = 30000
NAVIGATION_TIMEOUT = 30000
WAIT_TIMEOUT = 10000

# Browser settings
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "500"))
VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

# Screenshot settings
TAKE_SCREENSHOTS = os.getenv("TAKE_SCREENSHOTS", "true").lower() == "true"
SCREENSHOT_DIR = "reports/screenshots"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
