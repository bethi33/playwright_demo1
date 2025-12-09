"""Product Page Objects"""
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class ProductPage:
    """Single product page interactions"""
    
    def __init__(self, page: Page):
        self.page = page
        # Product details
        self.product_name = page.locator("h1").first
        self.product_price = page.locator(".price").first
        self.product_description = page.locator(".description").first
        self.product_rating = page.locator(".rating")
        
        # Product options
        self.quantity_input = page.get_by_label("Qty")
        self.add_to_cart_button = page.get_by_role("button", name="Add to Cart")
        self.add_to_wishlist_button = page.locator("button[title='Add to Wish List']").first
        
        # Product images
        self.main_image = page.locator(".product-image-container img").first
        self.thumbnail_images = page.locator(".product-thumb-image")
        
        # Stock status
        self.stock_status = page.locator(".availability-status").first
        
    def get_product_name(self) -> str:
        """Get product name"""
        name = self.product_name.inner_text()
        logger.info(f"Product name: {name}")
        return name
    
    def get_product_price(self) -> str:
        """Get product price"""
        price = self.product_price.inner_text()
        logger.info(f"Product price: {price}")
        return price
    
    def set_quantity(self, quantity: int):
        """Set product quantity"""
        logger.info(f"Setting quantity to: {quantity}")
        self.quantity_input.clear()
        self.quantity_input.fill(str(quantity))
    
    def add_to_cart(self):
        """Add product to cart"""
        logger.info("Adding product to cart")
        self.add_to_cart_button.click()
        
    def add_to_wishlist(self):
        """Add product to wishlist"""
        logger.info("Adding product to wishlist")
        self.add_to_wishlist_button.click()
        
    def get_stock_status(self) -> str:
        """Get product stock status"""
        status = self.stock_status.inner_text()
        logger.info(f"Stock status: {status}")
        return status
    
    def is_product_in_stock(self) -> bool:
        """Check if product is in stock"""
        stock = self.stock_status.inner_text()
        in_stock = "in stock" in stock.lower()
        logger.info(f"In stock: {in_stock}")
        return in_stock


class ProductListPage:
    """Product listing/catalog page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.product_items = page.locator(".product-thumb")
        self.product_links = page.locator(".product-thumb a[href*='product']")
        self.sort_dropdown = page.locator("select[name='sort']")
        self.limit_dropdown = page.locator("select[name='limit']")
        self.filter_buttons = page.locator(".filter-group button")
        self.price_filter_min = page.get_by_label("Min Price")
        self.price_filter_max = page.get_by_label("Max Price")
        self.apply_filter_button = page.get_by_role("button", name="Apply")
        
    def get_products_count(self) -> int:
        """Get number of products displayed"""
        count = self.product_items.count()
        logger.info(f"Products displayed: {count}")
        return count
    
    def click_product(self, product_index: int):
        """Click on a product by index"""
        logger.info(f"Clicking product at index {product_index}")
        self.product_links.nth(product_index).click()
    
    def sort_products(self, sort_option: str):
        """Sort products by option"""
        logger.info(f"Sorting products by: {sort_option}")
        self.sort_dropdown.select_option(sort_option)
    
    def set_products_per_page(self, limit: str):
        """Set number of products per page"""
        logger.info(f"Setting products per page to: {limit}")
        self.limit_dropdown.select_option(limit)
    
    def filter_by_price(self, min_price: str, max_price: str):
        """Filter products by price range"""
        logger.info(f"Filtering by price: {min_price} - {max_price}")
        self.price_filter_min.fill(min_price)
        self.price_filter_max.fill(max_price)
        self.apply_filter_button.click()
    
    def search_in_list(self, search_term: str):
        """Search within product list"""
        logger.info(f"Searching in list: {search_term}")
        search_input = self.page.get_by_placeholder("Search")
        search_input.fill(search_term)
        search_input.locator("..").get_by_role("button").click()
