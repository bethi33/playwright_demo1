from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class HomePage:

    def __init__(self, page: Page):
        self.page = page

        self.logo = page.locator("a[href*='home']").first
        self.shop_button = page.get_by_role("link", name="Shop").first
        self.my_account_dropdown = page.get_by_role("button", name="My account")
        self.register_link = page.get_by_role("link", name="Register").first
        self.login_link = page.get_by_role("link", name="Login")
        self.search_input = page.get_by_placeholder("Search")
        self.search_button = page.get_by_role("button", name="Search")


        self.cart_link = page.locator("a[href*='cart']").first
        self.cart_icon = page.locator(".fa-shopping-cart").first


        self.featured_products = page.locator(".product-thumb")

    def navigate_to_home(self):
        logger.info("Navigating to homepage")
        self.page.goto("https://ecommerce-playground.lambdatest.io/")

    def search_product(self, product_name: str):
        logger.info(f"Searching for product: {product_name}")
        self.search_input.fill(product_name)
        self.search_button.click()

    def navigate_to_shop(self):
        logger.info("Navigating to shop")
        self.shop_button.click()

    def navigate_to_cart(self):
        logger.info("Navigating to cart")
        self.cart_link.click()

    def open_my_account_menu(self):
        logger.info("Opening my account menu")
        self.my_account_dropdown.hover()

    def navigate_to_registration(self):
        logger.info("Navigating to registration")
        self.my_account_dropdown.hover()
        self.register_link.click()

    def navigate_to_login(self):
        logger.info("Navigating to login")
        self.my_account_dropdown.hover()
        self.login_link.click()

    def get_featured_products_count(self):
        count = self.featured_products.count()
        logger.info(f"Featured products count: {count}")
        return count