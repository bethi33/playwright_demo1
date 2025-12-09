"""Shopping Cart and Checkout Page Objects"""
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class CartPage:
    """Shopping cart page interactions"""

    def __init__(self, page: Page):
        self.page = page

        self.cart_items = page.locator("table tbody tr")
        self.item_names = page.locator(".product-name")
        self.item_quantities = page.locator("input[name*='quantity']")
        self.item_prices = page.locator(".product-price")
        self.remove_buttons = page.locator("button[title='Remove']")


        self.subtotal = page.locator(".subtotal-amount")
        self.tax_amount = page.locator(".tax-amount")
        self.total_amount = page.locator(".total-amount")


        self.continue_shopping_button = page.get_by_role("link", name="Continue Shopping")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.update_cart_button = page.get_by_role("button", name="Update Cart")


        self.coupon_input = page.locator("input[name='coupon']")
        self.apply_coupon_button = page.get_by_role("button", name="Apply Coupon")

    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        count = self.cart_items.count()
        logger.info(f"Cart items count: {count}")
        return count

    def update_item_quantity(self, item_index: int, quantity: int):
        """Update quantity of item in cart"""
        logger.info(f"Updating item {item_index} quantity to {quantity}")
        self.item_quantities.nth(item_index).clear()
        self.item_quantities.nth(item_index).fill(str(quantity))
        self.update_cart_button.click()

    def remove_item(self, item_index: int):
        """Remove item from cart"""
        logger.info(f"Removing item at index {item_index}")
        self.remove_buttons.nth(item_index).click()

    def get_subtotal(self) -> str:
        """Get subtotal amount"""
        amount = self.subtotal.inner_text()
        logger.info(f"Subtotal: {amount}")
        return amount

    def get_total(self) -> str:
        """Get total amount"""
        amount = self.total_amount.inner_text()
        logger.info(f"Total: {amount}")
        return amount

    def apply_coupon(self, coupon_code: str):
        """Apply discount coupon"""
        logger.info(f"Applying coupon: {coupon_code}")
        self.coupon_input.fill(coupon_code)
        self.apply_coupon_button.click()

    def proceed_to_checkout(self):
        """Proceed to checkout"""
        logger.info("Proceeding to checkout")
        self.checkout_button.click()

    def is_empty(self) -> bool:
        """Check if cart is empty"""
        count = self.get_cart_items_count()
        return count == 0


class CheckoutPage:
    """Checkout page interactions"""

    def __init__(self, page: Page):
        self.page = page

        self.billing_firstname = page.get_by_label("First Name")
        self.billing_lastname = page.get_by_label("Last Name")
        self.billing_email = page.get_by_label("E-Mail")
        self.billing_phone = page.get_by_label("Telephone")
        self.billing_company = page.get_by_label("Company")
        self.billing_address1 = page.get_by_label("Address 1")
        self.billing_address2 = page.get_by_label("Address 2")
        self.billing_city = page.get_by_label("City")
        self.billing_postcode = page.get_by_label("Post Code")
        self.billing_country = page.locator("select[name='country_id']").first
        self.billing_state = page.locator("select[name='zone_id']").first


        self.shipping_checkbox = page.locator("input[name='shipping_address']")
        self.shipping_firstname = page.get_by_label("Shipping First Name")
        self.shipping_lastname = page.get_by_label("Shipping Last Name")


        self.shipping_methods = page.locator("input[name='shipping_method']")


        self.payment_methods = page.locator("input[name='payment_method']")


        self.continue_button = page.get_by_role("button", name="Continue")
        self.confirm_button = page.get_by_role("button", name="Confirm Order")
        self.confirm_order_button = page.get_by_role("button", name="Confirm Order")

    def fill_billing_address(self, first_name: str, last_name: str, email: str, 
                            phone: str, address: str, city: str, postcode: str):
        """Fill billing address form"""
        logger.info(f"Filling billing address for {first_name} {last_name}")
        self.billing_firstname.fill(first_name)
        self.billing_lastname.fill(last_name)
        self.billing_email.fill(email)
        self.billing_phone.fill(phone)
        self.billing_address1.fill(address)
        self.billing_city.fill(city)
        self.billing_postcode.fill(postcode)

    def select_country(self, country_name: str):
        """Select country"""
        logger.info(f"Selecting country: {country_name}")
        self.billing_country.select_option(country_name)

    def select_state(self, state_id: str):
        """Select state/province"""
        logger.info(f"Selecting state: {state_id}")
        self.billing_state.select_option(state_id)

    def select_shipping_method(self, method_index: int):
        """Select shipping method"""
        logger.info(f"Selecting shipping method at index {method_index}")
        self.shipping_methods.nth(method_index).check()

    def select_payment_method(self, method_index: int):
        """Select payment method"""
        logger.info(f"Selecting payment method at index {method_index}")
        self.payment_methods.nth(method_index).check()

    def confirm_order(self):
        """Confirm and place order"""
        logger.info("Confirming order")
        self.confirm_order_button.click()

    def continue_to_next_step(self):
        """Continue to next step"""
        logger.info("Continuing to next step")
        self.continue_button.click()