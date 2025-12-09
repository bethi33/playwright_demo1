import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages import HomePage, ProductPage, ProductListPage, CartPage, CheckoutPage

CATEGORY_PATH = f"{BASE_URL}/index.php?route=product/category&path=20"
LOGIN_PATH = f"{BASE_URL}/index.php?route=account/login"


class TestShoppingCart:
    
    def test_add_product_to_cart(self, page: Page):
        """Test adding a product to cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        expect(page.locator(".alert-success")).to_be_visible()
    
    def test_add_multiple_products_to_cart(self, page: Page):
        """Test adding multiple products to cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        
        product_list.click_product(0)
        product_page = ProductPage(page)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")
        
        page.go_back()
        page.wait_for_load_state("networkidle")
        product_list.click_product(1)
        product_page.add_to_cart()
        page.wait_for_load_state("networkidle")
        
        expect(page.locator(".alert-success")).to_be_visible()
    
    def test_view_cart(self, page: Page):
        """Test viewing shopping cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        items_count = cart_page.get_cart_items_count()
        assert items_count > 0, "Cart should have items"
    
    def test_update_cart_quantity(self, page: Page):
        """Test updating item quantity in cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.update_item_quantity(0, 3)
        page.wait_for_load_state("networkidle")
        
        quantity = cart_page.item_quantities.nth(0).input_value()
        assert quantity == "3", "Quantity not updated"
    
    def test_remove_product_from_cart(self, page: Page):
        """Test removing product from cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        initial_count = cart_page.get_cart_items_count()
        
        cart_page.remove_item(0)
        page.wait_for_load_state("networkidle")
        
        final_count = cart_page.get_cart_items_count()
        assert final_count < initial_count, "Item not removed from cart"
    
    def test_cart_displays_total(self, page: Page):
        """Test cart displays total amount"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        total = cart_page.get_total()
        assert total and len(total) > 0, "Total not displayed"
    
    def test_add_to_wishlist(self, page: Page):
        """Test adding product to wishlist"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_wishlist()
        
        page.wait_for_load_state("networkidle")
        expect(page.locator(".alert-success")).to_be_visible()
    
    def test_apply_coupon_code(self, page: Page, login_credentials):
        """Test applying coupon code to cart"""
        page.goto(CATEGORY_PATH)
        
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.apply_coupon("TESTCOUPON")
        
        page.wait_for_load_state("networkidle")
        # Check if alert appears (success or error)
        alert = page.locator(".alert")
        assert alert.is_visible(), "No response from coupon application"


class TestCheckout:
    
    def test_checkout_page_loads(self, page: Page, login_credentials):
        """Test checkout page loads correctly"""
        page.goto(LOGIN_PATH)
        
        # Login first
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        # Add product to cart
        page.goto(CATEGORY_PATH)
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        
        # Go to checkout
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("**/checkout")
    
    def test_fill_billing_address(self, page: Page, login_credentials):
        """Test filling billing address during checkout"""
        page.goto(LOGIN_PATH)
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        # Add product and go to checkout
        page.goto(CATEGORY_PATH)
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        
        page.wait_for_load_state("networkidle")
        
        checkout_page = CheckoutPage(page)
        checkout_page.fill_billing_address(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="New York",
            postcode="10001"
        )
    
    def test_select_shipping_method(self, page: Page, login_credentials):
        """Test selecting shipping method"""
        page.goto(LOGIN_PATH)
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        # Add product and checkout
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        
        page.wait_for_load_state("networkidle")
        
        checkout_page = CheckoutPage(page)
        # Select first available shipping method
        if checkout_page.shipping_methods.count() > 0:
            checkout_page.select_shipping_method(0)
    
    def test_select_payment_method(self, page: Page, login_credentials):
        """Test selecting payment method"""
        page.goto(LOGIN_PATH)
        
        # Login
        page.get_by_role("textbox", name="E-Mail").fill(login_credentials["valid_email"])
        page.get_by_role("textbox", name="Password").fill(login_credentials["valid_password"])
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_load_state("networkidle")
        
        # Add product and checkout
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
        product_list = ProductListPage(page)
        product_list.click_product(0)
        
        product_page = ProductPage(page)
        product_page.add_to_cart()
        
        page.wait_for_load_state("networkidle")
        home_page = HomePage(page)
        home_page.navigate_to_cart()
        
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        
        page.wait_for_load_state("networkidle")
        
        checkout_page = CheckoutPage(page)
        # Select first available payment method
        if checkout_page.payment_methods.count() > 0:
            checkout_page.select_payment_method(0)
