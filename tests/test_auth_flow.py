from playwright.sync_api import Page, expect
from config import BASE_URL
from pages.lamdatest_login_page import LoginPage
from pages.lamdatest_home_page import HomePage
from pages.lamdatest_register_page import RegisterPage
from faker import Faker

fake = Faker()
LOGIN_PATH = f"{BASE_URL}/index.php?route=account/login"
HOME_PATH = f"{BASE_URL}/index.php?route=common/home"

def test_valid_login(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_PATH)
    login_page.login("sssdjsd@gmail.com", "123456")

    expect(page).to_have_title("My Account")

def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    page.goto(LOGIN_PATH)
    login_page.login("wronguser@example.com", "wrongpassword")

    expect(page.locator(".alert-danger")).to_be_visible()

def test_user_registration(page: Page):
    home_page = HomePage(page)
    register_page = RegisterPage(page)

    page.goto(HOME_PATH)
    home_page.navigate_to_registration()

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    telephone = fake.phone_number()
    password = "Password123!"

    register_page.register_user(first_name, last_name, email, telephone, password)

    expect(page).to_have_title("Your Account Has Been Created!")
    expect(page.get_by_text("Your Account Has Been Created!")).to_be_visible()