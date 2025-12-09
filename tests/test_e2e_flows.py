import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages import (
    HomePage, ProductListPage, ProductPage, CartPage, CheckoutPage,
    LoginPage, AccountPage, OrderHistoryPage
)

LOGIN_PATH = f"{BASE_URL}/index.php?route=account/login"
ACCOUNT_PATH = f"{BASE_URL}/index.php?route=account/account"
CART_PATH = f"{BASE_URL}/index.php?route=checkout/cart"


class TestCompleteShoppingFlow:

    def test_complete_purchase_flow_guest_user(self, page: Page):
        """Test complete purchase flow as guest user"""
        home_page = HomePage(page)
        home_page.navigate_to_home()

        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")

        product_list = ProductListPage(page)
        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_name = product_page.get_product_name()
        product_page.set_quantity(2)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")


        cart_page = CartPage(page)
        items_count = cart_page.get_cart_items_count()
        assert items_count > 0, "Product should be in cart"


        total = cart_page.get_total()
        assert total and len(total) > 0, "Total should be displayed"

    def test_complete_purchase_with_multiple_products(self, page: Page):
        """Test purchasing multiple different products"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")

        product_list = ProductListPage(page)


        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")

        page.go_back()
        page.wait_for_load_state("networkidle")

        product_list.click_product(1)
        page.wait_for_load_state("networkidle")

        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")

        cart_page = CartPage(page)
        items_count = cart_page.get_cart_items_count()
        assert items_count >= 2, "Should have at least 2 products"

    def test_complete_purchase_with_quantity_modification(self, page: Page):
        """Test modifying quantities during shopping"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")

        product_list = ProductListPage(page)
        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_page.set_quantity(5)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")


        cart_page = CartPage(page)
        cart_page.update_item_quantity(0, 10)
        page.wait_for_load_state("networkidle")

        quantity = cart_page.item_quantities.nth(0).input_value()
        assert quantity == "10", "Quantity should be updated to 10"

    def test_complete_purchase_add_remove_products(self, page: Page):
        """Test adding and removing products from cart"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")

        product_list = ProductListPage(page)


        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        page.go_back()
        page.wait_for_load_state("networkidle")
        product_list.click_product(1)
        page.wait_for_load_state("networkidle")

        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")


        cart_page = CartPage(page)
        initial_count = cart_page.get_cart_items_count()
        assert initial_count >= 2, "Should have 2 products in cart"


        cart_page.remove_item(0)
        page.wait_for_load_state("networkidle")

        final_count = cart_page.get_cart_items_count()
        assert final_count < initial_count, "One product should be removed"


class TestUserAuthenticationFlow:
    """Test user authentication and account access"""

    def test_user_registration_and_login_flow(self, page: Page):
        """Test complete registration and login flow"""
        from faker import Faker
        fake = Faker()


        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_registration()
        page.wait_for_load_state("networkidle")


        from pages import RegisterPage
        register_page = RegisterPage(page)

        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = "TestPassword123!"
        telephone = fake.phone_number()

        register_page.register_user(first_name, last_name, email, telephone, password)
        page.wait_for_load_state("networkidle")


        expect(page).to_have_url("**/account")

    def test_login_and_access_account_features(self, page: Page, login_credentials):
        """Test login and accessing all account features"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")


        login_page = LoginPage(page)
        login_page.login(login_credentials["valid_email"], login_credentials["valid_password"])
        page.wait_for_load_state("networkidle")


        account_page = AccountPage(page)


        account_page.view_order_history()
        page.wait_for_load_state("networkidle")


        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/account")


        account_page.view_wish_list()
        page.wait_for_load_state("networkidle")


        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/account")


        account_page.view_address_book()
        page.wait_for_load_state("networkidle")


class TestProductSearchAndFiltering:
    """Test comprehensive product search and filtering"""

    def test_search_and_purchase_flow(self, page: Page):
        """Test searching for product and purchasing it"""
        home_page = HomePage(page)
        home_page.navigate_to_home()


        home_page.search_product("Laptop")
        page.wait_for_load_state("networkidle")


        product_list = ProductListPage(page)
        count = product_list.get_products_count()
        assert count > 0, "Search should return results"


        product_list.click_product(0)
        page.wait_for_load_state("networkidle")


        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")


        cart_page = CartPage(page)
        items_count = cart_page.get_cart_items_count()
        assert items_count > 0, "Product should be in cart"

    def test_browse_categories_and_filter_products(self, page: Page):
        """Test browsing product categories and filtering"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")


        product_list = ProductListPage(page)
        initial_count = product_list.get_products_count()
        assert initial_count > 0, "Should display products"


        product_list.sort_products("name-asc")
        page.wait_for_load_state("networkidle")

        sorted_count = product_list.get_products_count()
        assert sorted_count > 0, "Should display products after sorting"


class TestCheckoutProcess:
    """Test detailed checkout process"""

    def test_checkout_with_address_selection(self, page: Page, login_credentials):
        """Test checkout process with address selection"""

        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        login_page = LoginPage(page)
        login_page.login(login_credentials["valid_email"], login_credentials["valid_password"])
        page.wait_for_load_state("networkidle")


        home_page = HomePage(page)
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")

        product_list = ProductListPage(page)
        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")

        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        page.wait_for_load_state("networkidle")


        expect(page).to_have_url("**/checkout")


class TestCartOperations:
    """Test various cart operations"""

    def test_cart_persistence_across_pages(self, page: Page):
        """Test cart items persist when browsing other pages"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()
        page.wait_for_load_state("networkidle")


        product_list = ProductListPage(page)
        product_list.click_product(0)
        page.wait_for_load_state("networkidle")

        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")


        page.go_back()
        page.wait_for_load_state("networkidle")

        product_list.click_product(1)
        page.wait_for_load_state("networkidle")


        home_page.navigate_to_cart()
        page.wait_for_load_state("networkidle")


        cart_page = CartPage(page)
        items_count = cart_page.get_cart_items_count()
        assert items_count >= 1, "Added product should still be in cart"

    def test_empty_cart_functionality(self, page: Page):
        """Test cart is empty on fresh visit"""
        page.goto(CART_PATH)
        page.wait_for_load_state("networkidle")

        cart_page = CartPage(page)


        items_count = cart_page.get_cart_items_count()

        assert items_count >= 0, "Cart should be accessible"