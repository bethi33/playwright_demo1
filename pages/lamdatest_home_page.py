from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.shop_button = page.get_by_role("link", name="Shop")
        self.my_account_link = page.get_by_role("button", name="My account")
        self.register_link = page.get_by_role("link", name="Register").first

    def click_shop(self):
        logger.info("Clicking Shop button")
        self.shop_button.click()    

    def navigate_to_registration(self):
        logger.info("Navigating to registration page")
        self.my_account_link.hover()
        self.register_link.click()