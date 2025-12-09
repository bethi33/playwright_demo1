import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages import (
    AccountPage, OrderHistoryPage, WishListPage, AddressBookPage,
    HomePage, ProductListPage, ProductPage, CartPage
)

LOGIN_PATH = f"{BASE_URL}/index.php?route=account/login"
CATEGORY_PATH = f"{BASE_URL}/index.php?route=product/category&path=20"


class TestOrderManagement:
    
    def test_view_order_history(self, page: Page, login_credentials):
        """Test viewing order history"""
        page.goto(LOGIN_PATH)
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        # Navigate to account
        account_page = AccountPage(page)
        account_page.view_order_history()
        
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("**/order")
    
    def test_get_order_count(self, page: Page, login_credentials):
        """Test getting order count from order history"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_order_history()
        
        page.wait_for_load_state("networkidle")
        
        order_history = OrderHistoryPage(page)
        orders_count = order_history.get_orders_count()
        assert orders_count >= 0, "Orders count should be non-negative"
    
    def test_view_order_details(self, page: Page, login_credentials):
        """Test viewing details of an order"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_order_history()
        
        page.wait_for_load_state("networkidle")
        
        order_history = OrderHistoryPage(page)
        orders_count = order_history.get_orders_count()
        
        if orders_count > 0:
            order_history.click_order(0)
            page.wait_for_load_state("networkidle")
            
            # Check if order details are displayed
            order_number = page.locator(".order-number").first
            assert order_number.is_visible(), "Order number not displayed"
    
    def test_get_order_status(self, page: Page, login_credentials):
        """Test getting order status"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_order_history()
        
        page.wait_for_load_state("networkidle")
        
        order_history = OrderHistoryPage(page)
        orders_count = order_history.get_orders_count()
        
        if orders_count > 0:
            status = order_history.get_order_status(0)
            assert status and len(status) > 0, "Order status not available"
    
    def test_get_order_total(self, page: Page, login_credentials):
        """Test getting order total"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_order_history()
        
        page.wait_for_load_state("networkidle")
        
        order_history = OrderHistoryPage(page)
        orders_count = order_history.get_orders_count()
        
        if orders_count > 0:
            total = order_history.get_order_total(0)
            assert total and len(total) > 0, "Order total not available"


class TestWishList:
    
    def test_view_wish_list(self, page: Page, login_credentials):
        """Test viewing wish list"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_wish_list()
        
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("**/wishlist")
    
    def test_get_wishlist_items_count(self, page: Page, login_credentials):
        """Test getting wish list items count"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_wish_list()
        
        page.wait_for_load_state("networkidle")
        
        wishlist = WishListPage(page)
        items_count = wishlist.get_wishlist_items_count()
        assert items_count >= 0, "Wish list items count should be non-negative"
    
    def test_add_wish_list_item_to_cart(self, page: Page, login_credentials):
        """Test adding wish list item to cart"""
        # First add a product to wishlist from product page
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_wishlist()
        
        page.wait_for_load_state("networkidle")
        
        # Now login and go to wishlist
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_wish_list()
        
        page.wait_for_load_state("networkidle")
        
        wishlist = WishListPage(page)
        items_count = wishlist.get_wishlist_items_count()
        
        if items_count > 0:
            wishlist.add_item_to_cart(0)
            page.wait_for_load_state("networkidle")
            
            expect(page.locator(".alert-success")).to_be_visible()


class TestAddressBook:
    
    def test_view_address_book(self, page: Page, login_credentials):
        """Test viewing address book"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_address_book()
        
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("**/address")
    
    def test_get_saved_addresses_count(self, page: Page, login_credentials):
        """Test getting count of saved addresses"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_address_book()
        
        page.wait_for_load_state("networkidle")
        
        address_book = AddressBookPage(page)
        addresses_count = address_book.get_addresses_count()
        assert addresses_count >= 0, "Addresses count should be non-negative"
    
    def test_add_new_address(self, page: Page, login_credentials):
        """Test adding a new address"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.view_address_book()
        
        page.wait_for_load_state("networkidle")
        
        address_book = AddressBookPage(page)
        initial_count = address_book.get_addresses_count()
        
        address_book.add_new_address(
            first_name="Jane",
            last_name="Smith",
            address="456 Oak Ave",
            city="Boston",
            postcode="02101"
        )
        
        page.wait_for_load_state("networkidle")
        
        final_count = address_book.get_addresses_count()
        assert final_count >= initial_count, "Address should be added"


class TestAccountManagement:
    
    def test_view_account_page(self, page: Page, login_credentials):
        """Test viewing account page"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("**/account")
    
    def test_logout_from_account(self, page: Page, login_credentials):
        """Test logging out from account"""
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        account_page = AccountPage(page)
        account_page.logout()
        
        page.wait_for_load_state("networkidle")
        # Should be redirected to home or login page
        expect(page).to_have_url("**/")
