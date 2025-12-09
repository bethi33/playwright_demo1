from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="E-Mail Address")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")

    def enter_username(self, username: str):    
        logger.info(f"Entering username: {username}")
        self.username_input.fill(username)

    def enter_password(self, password: str):    
        logger.info("Entering password")
        self.password_input.fill(password)

    def click_login(self):    
        logger.info("Clicking login button")
        self.login_button.click()
    
    def is_forgot_password_link_visible(self):
        is_visible = self.page.locator("a[href*='forgotten']").is_visible()
        logger.info(f"Forgot password link visible: {is_visible}")
        return is_visible

    def get_alert_message(self):
        logger.info("Retrieving alert message")
        return self.page.locator(".alert-danger")
    
    def click_logout(self):
        logger.info("Clicking logout")
        self.page.click("a[href*='logout']")
    
    def login(self, username: str, password: str):    
        logger.info(f"Performing login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        
