import re
from playwright.sync_api import Page, expect
from pages.lamdatest_login_page import LoginPage

BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php"
LOGIN_URL = f"{BASE_URL}?route=account/login"

VALID_EMAIL = "sssdjsd@gmail.com"
VALID_PASSWORD = "123456"
INVALID_EMAIL = "ssssdjddsd@gmail.com"
INVALID_PASSWORD = "wrongpass"


def test_login_page_ui(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)

    expect(page).to_have_title("Account Login")
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()


def test_valid_login(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    login_page.login(VALID_EMAIL, VALID_PASSWORD)

    expect(page).to_have_url(f"{BASE_URL}?route=account/account")
    expect(page.locator("h2")).to_contain_text("My Account")


def test_invalid_password(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)

    login_page.login(VALID_EMAIL, INVALID_PASSWORD)

    expect(login_page.get_alert_message()).to_be_visible()


def test_invalid_email(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.login(INVALID_EMAIL, VALID_PASSWORD)

    expect(login_page.get_alert_message()).to_be_visible()


def test_forgot_password_link_visible(page: Page):
    """Test forgot password link is visible on login page"""
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    assert login_page.is_forgot_password_link_visible(), "Forgot password link should be visible"


def test_login_with_empty_credentials(page: Page):
    """Test login with empty email and password"""
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.click_login()
    # Most websites require field validation
    expect(login_page.username_input).to_be_focused()
def test_empty_email_and_password(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.click_login()

    expect(login_page.get_alert_message()).to_be_visible()


def test_empty_email(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.enter_password(VALID_PASSWORD)
    login_page.click_login()

    expect(login_page.get_alert_message()).to_be_visible()


def test_empty_password(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.enter_username(VALID_EMAIL)
    login_page.click_login()

    expect(login_page.get_alert_message()).to_be_visible()


def test_password_masked(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)

    expect(login_page.password_input).to_have_attribute("type", "password")


def test_forgot_password_link_visible(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)

    assert login_page.is_forgot_password_link_visible()


def test_logout_after_login(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    
    login_page.click_logout()
    expect(page).to_have_url(f"{BASE_URL}?route=account/logout")
