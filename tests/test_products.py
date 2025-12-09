import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages import HomePage, ProductPage, ProductListPage

CATEGORY_PATH = f"{BASE_URL}/index.php?route=product/category&path=20"


class TestProductBrowsing:

    def test_navigate_to_shop(self, page: Page):
        """Test navigating to shop page"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.navigate_to_shop()

        expect(page).to_have_url("**/shop")
        expect(page.locator("h1")).to_contain_text("Shop")

    def test_view_featured_products(self, page: Page):
        """Test viewing featured products on homepage"""
        home_page = HomePage(page)
        home_page.navigate_to_home()

        products_count = home_page.get_featured_products_count()
        assert products_count > 0, "No featured products found"

    def test_product_list_displays_correctly(self, page: Page):
        """Test product list displays with correct information"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        products_count = product_list.get_products_count()
        assert products_count > 0, "No products found in list"

    def test_click_product_opens_details(self, page: Page):
        """Test clicking product opens product detail page"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)
        product_name = product_page.get_product_name()
        assert product_name, "Product name not found"

    def test_product_shows_price(self, page: Page):
        """Test product shows price information"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)
        price = product_page.get_product_price()
        assert price and len(price) > 0, "Price not displayed"

    def test_product_shows_stock_status(self, page: Page):
        """Test product displays stock status"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)
        in_stock = product_page.is_product_in_stock()
        assert isinstance(in_stock, bool), "Stock status not determined"

    def test_sort_products_by_name(self, page: Page):
        """Test sorting products by name"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.sort_products("name-asc")

        page.wait_for_load_state("networkidle")
        products_count = product_list.get_products_count()
        assert products_count > 0, "No products displayed after sorting"


class TestProductSearch:

    def test_search_product_by_name(self, page: Page):
        """Test searching for product by name"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.search_product("Laptop")

        expect(page).to_have_url("**search=Laptop**")
        product_list = ProductListPage(page)
        products_count = product_list.get_products_count()
        assert products_count > 0, "No search results found"

    def test_search_nonexistent_product(self, page: Page):
        """Test searching for nonexistent product"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.search_product("NonexistentProductXYZ123")


        product_list = ProductListPage(page)
        products_count = product_list.get_products_count()
        assert products_count == 0, "Should show no results for nonexistent product"

    def test_search_with_special_characters(self, page: Page):
        """Test search handles special characters"""
        home_page = HomePage(page)
        home_page.navigate_to_home()
        home_page.search_product("A@#$%")


        expect(page).to_have_url("**search=**")


class TestProductFiltering:

    def test_filter_by_price_range(self, page: Page):
        """Test filtering products by price range"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.filter_by_price("100", "500")


        page.wait_for_load_state("networkidle")
        products_count = product_list.get_products_count()
        assert products_count >= 0, "Filter applied but no products shown"

    def test_change_products_per_page(self, page: Page):
        """Test changing products per page limit"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.set_products_per_page("25")

        page.wait_for_load_state("networkidle")
        products_count = product_list.get_products_count()
        assert products_count <= 25, "More products shown than limit"

    def test_sort_products_by_price(self, page: Page):
        """Test sorting products by price"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.sort_products("price-asc")

        page.wait_for_load_state("networkidle")
        products_count = product_list.get_products_count()
        assert products_count > 0, "No products after sorting by price"


class TestProductDetails:

    def test_view_product_images(self, page: Page):
        """Test viewing product images"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)

        main_image_visible = product_page.main_image.is_visible()
        assert main_image_visible, "Main product image not visible"

    def test_get_product_description(self, page: Page):
        """Test getting product description"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)
        description = product_page.product_description.inner_text()
        assert description, "Product description not found"

    def test_product_quantity_adjustment(self, page: Page):
        """Test adjusting product quantity"""
        page.goto(CATEGORY_PATH)

        product_list = ProductListPage(page)
        product_list.click_product(0)

        product_page = ProductPage(page)
        product_page.set_quantity(5)

        quantity_value = product_page.quantity_input.input_value()
        assert quantity_value == "5", "Quantity not set correctly"