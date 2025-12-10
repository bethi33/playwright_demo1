from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class AccountPage:

    def __init__(self, page: Page):
        self.page = page

        self.edit_account_link = page.get_by_role("link", name="Edit Account")
        self.change_password_link = page.get_by_role("link", name="Change Password")
        self.address_book_link = page.get_by_role("link", name="Address Book")
        self.wish_list_link = page.get_by_role("link", name="Wish List")
        self.order_history_link = page.get_by_role("link", name="Order History")
        self.downloads_link = page.get_by_role("link", name="Downloads")
        self.logout_link = page.get_by_role("link", name="Logout")


        self.account_name = page.locator(".account-name").first
        self.account_email = page.locator(".account-email").first

    def edit_account(self):
        logger.info("Going to edit account")
        self.edit_account_link.click()

    def change_password(self):
        logger.info("Going to change password")
        self.change_password_link.click()

    def view_address_book(self):
        logger.info("Going to address book")
        self.address_book_link.click()

    def view_wish_list(self):
        logger.info("Going to wish list")
        self.wish_list_link.click()

    def view_order_history(self):
        logger.info("Going to order history")
        self.order_history_link.click()

    def logout(self):
        logger.info("Logging out")
        self.logout_link.click()


class OrderHistoryPage:

    def __init__(self, page: Page):
        self.page = page

        self.orders_table = page.locator("table tbody tr")
        self.order_ids = page.locator("a[href*='order/info']")
        self.order_dates = page.locator(".order-date")
        self.order_totals = page.locator(".order-total")
        self.order_statuses = page.locator(".order-status")


        self.order_number = page.locator(".order-number").first
        self.order_date = page.locator(".order-date-detail").first
        self.order_items = page.locator("table.order-items tbody tr")
        self.order_subtotal = page.locator(".subtotal-amount")
        self.order_tax = page.locator(".tax-amount")
        self.order_total = page.locator(".total-amount")
        self.order_status = page.locator(".status-badge")


        self.reorder_button = page.get_by_role("button", name="Reorder")
        self.view_order_button = page.get_by_role("link", name="View")
        self.download_invoice_button = page.get_by_role("button", name="Download Invoice")

    def get_orders_count(self) -> int:
        count = self.orders_table.count()
        logger.info(f"Orders count: {count}")
        return count

    def click_order(self, order_index: int):
        logger.info(f"Clicking order at index {order_index}")
        self.order_ids.nth(order_index).click()

    def get_order_status(self, order_index: int) -> str:
        status = self.order_statuses.nth(order_index).inner_text()
        logger.info(f"Order status: {status}")
        return status

    def get_order_total(self, order_index: int) -> str:
        total = self.order_totals.nth(order_index).inner_text()
        logger.info(f"Order total: {total}")
        return total

    def reorder_product(self):
        logger.info("Reordering product")
        self.reorder_button.click()

    def download_invoice(self):
        logger.info("Downloading invoice")
        self.download_invoice_button.click()

    def get_order_items_count(self) -> int:
        count = self.order_items.count()
        logger.info(f"Order items count: {count}")
        return count


class WishListPage:

    def __init__(self, page: Page):
        self.page = page
        self.wishlist_items = page.locator("table tbody tr")
        self.item_names = page.locator(".product-name")
        self.item_prices = page.locator(".product-price")
        self.add_to_cart_buttons = page.get_by_role("button", name="Add to Cart")
        self.remove_buttons = page.locator("button[title='Remove']")

    def get_wishlist_items_count(self) -> int:
        count = self.wishlist_items.count()
        logger.info(f"Wish list items count: {count}")
        return count

    def add_item_to_cart(self, item_index: int):
        logger.info(f"Adding wish list item {item_index} to cart")
        self.add_to_cart_buttons.nth(item_index).click()

    def remove_item(self, item_index: int):
        logger.info(f"Removing wish list item {item_index}")
        self.remove_buttons.nth(item_index).click()


class AddressBookPage:

    def __init__(self, page: Page):
        self.page = page
        self.addresses = page.locator(".address-item")
        self.add_address_button = page.get_by_role("button", name="Add Address")
        self.edit_buttons = page.get_by_role("link", name="Edit")
        self.delete_buttons = page.get_by_role("button", name="Delete")


        self.firstname = page.get_by_label("First Name")
        self.lastname = page.get_by_label("Last Name")
        self.address1 = page.get_by_label("Address 1")
        self.city = page.get_by_label("City")
        self.postcode = page.get_by_label("Post Code")
        self.country = page.locator("select[name='country_id']")
        self.state = page.locator("select[name='zone_id']")
        self.save_button = page.get_by_role("button", name="Save")

    def get_addresses_count(self) -> int:
        count = self.addresses.count()
        logger.info(f"Addresses count: {count}")
        return count

    def add_new_address(self, first_name: str, last_name: str, address: str, city: str, postcode: str):
        logger.info(f"Adding new address for {first_name} {last_name}")
        self.add_address_button.click()
        self.firstname.fill(first_name)
        self.lastname.fill(last_name)
        self.address1.fill(address)
        self.city.fill(city)
        self.postcode.fill(postcode)
        self.save_button.click()

    def edit_address(self, address_index: int):
        logger.info(f"Editing address at index {address_index}")
        self.edit_buttons.nth(address_index).click()

    def delete_address(self, address_index: int):
        logger.info(f"Deleting address at index {address_index}")
        self.delete_buttons.nth(address_index).click()