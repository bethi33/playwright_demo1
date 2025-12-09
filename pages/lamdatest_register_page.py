from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.email_input = page.get_by_placeholder("E-Mail")
        self.telephone_input = page.get_by_placeholder("Telephone")
        self.password_input = page.get_by_placeholder("Password", exact=True)
        self.confirm_password_input = page.get_by_placeholder("Password Confirm")
        self.privacy_policy_checkbox = page.get_by_label("I have read and agree to the Privacy Policy")
        self.continue_button = page.get_by_role("button", name="Continue")
        
    def register_user(self, first_name, last_name, email, telephone, password):
        logger.info(f"Registering user: {email}")
        self.first_name_input.fill(first_name)
        logger.info(f"Filled first name: {first_name}")
        self.last_name_input.fill(last_name)
        logger.info(f"Filled last name: {last_name}")
        self.email_input.fill(email)
        logger.info(f"Filled email: {email}")
        self.telephone_input.fill(telephone)
        logger.info(f"Filled telephone: {telephone}")
        self.password_input.fill(password)
        logger.info("Filled password")
        self.confirm_password_input.fill(password)
        logger.info("Filled password confirmation")
        self.privacy_policy_checkbox.check()
        logger.info("Checked privacy policy checkbox")
        self.continue_button.click()
        logger.info("Clicked continue button")

