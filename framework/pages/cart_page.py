"""
Cart page object implementing the Page Object Model pattern.
Contains all elements and actions related to the shopping cart page.
"""

from typing import List, Dict
from playwright.sync_api import Page
from framework.pages.base_page import BasePage
import allure


class CartPage(BasePage):
    """Cart page object for SauceDemo application."""
    
    # Page elements - MCP verified selectors
    PAGE_TITLE = '[data-test="title"]'  # Confirmed via MCP
    CART_CONTENTS_CONTAINER = '[data-test="cart-contents-container"]'  # Confirmed via MCP
    CART_LIST = '[data-test="cart-list"]'  # Confirmed via MCP
    CART_ITEM = '[data-test="inventory-item"]'  # Confirmed via MCP (in cart context)
    CART_ITEM_NAME = '[data-test="inventory-item-name"]'  # Confirmed via MCP
    CART_ITEM_PRICE = '[data-test="inventory-item-price"]'  # Confirmed via MCP
    CART_ITEM_DESC = '[data-test="inventory-item-desc"]'  # Confirmed via MCP
    CART_QUANTITY = '[data-test="item-quantity"]'  # Confirmed via MCP
    CART_QUANTITY_LABEL = '[data-test="cart-quantity-label"]'  # Confirmed via MCP
    CART_DESC_LABEL = '[data-test="cart-desc-label"]'  # Confirmed via MCP
    REMOVE_BUTTON = '[data-test^="remove"]'  # Confirmed via MCP
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'  # Confirmed via MCP
    CHECKOUT_BUTTON = '[data-test="checkout"]'  # Confirmed via MCP
    CART_FOOTER = '.cart_footer'  # Confirmed via MCP
    
    # Header elements
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'  # Confirmed via MCP
    
    def __init__(self, page: Page):
        """
        Initialize the cart page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.url = f"{self.config.base_url}/cart.html"
    
    def is_loaded(self) -> bool:
        """
        Check if the cart page is loaded.
        
        Returns:
            True if cart page is loaded, False otherwise
        """
        return (self.is_element_visible(self.PAGE_TITLE) and 
                self.get_text(self.PAGE_TITLE) == "Your Cart")
    
    @allure.step("Verify Your Cart page is displayed")
    def verify_cart_page(self) -> bool:
        """
        Verify that the Your Cart page is displayed correctly.
        
        Returns:
            True if Your Cart page is displayed, False otherwise
        """
        return (self.is_element_visible(self.PAGE_TITLE) and 
                "Your Cart" in self.get_text(self.PAGE_TITLE))
    
    @allure.step("Get cart item count")
    def get_cart_item_count(self) -> int:
        """
        Get the number of items in the cart.
        
        Returns:
            Number of items in cart
        """
        return len(self.page.locator(self.CART_ITEM).all())
    
    @allure.step("Get cart item names")
    def get_cart_item_names(self) -> List[str]:
        """
        Get all item names in the cart.
        
        Returns:
            List of item names
        """
        item_elements = self.page.locator(self.CART_ITEM_NAME).all()
        return [element.text_content() or "" for element in item_elements]
    
    @allure.step("Get cart item prices")
    def get_cart_item_prices(self) -> List[str]:
        """
        Get all item prices in the cart.
        
        Returns:
            List of item prices
        """
        price_elements = self.page.locator(self.CART_ITEM_PRICE).all()
        return [element.text_content() or "" for element in price_elements]
    
    @allure.step("Get cart item quantities")
    def get_cart_item_quantities(self) -> List[int]:
        """
        Get all item quantities in the cart.
        
        Returns:
            List of item quantities
        """
        quantity_elements = self.page.locator(self.CART_QUANTITY).all()
        quantities = []
        for element in quantity_elements:
            qty_text = element.text_content() or "0"
            quantities.append(int(qty_text) if qty_text.isdigit() else 0)
        return quantities
    
    @allure.step("Get cart items details")
    def get_cart_items_details(self) -> List[Dict[str, str]]:
        """
        Get detailed information about all items in the cart.
        
        Returns:
            List of dictionaries containing item details
        """
        items = []
        cart_items = self.page.locator(self.CART_ITEM).all()
        
        for item in cart_items:
            name_element = item.locator(self.CART_ITEM_NAME)
            price_element = item.locator(self.CART_ITEM_PRICE)
            quantity_element = item.locator(self.CART_QUANTITY)
            
            item_details = {
                "name": name_element.text_content() or "",
                "price": price_element.text_content() or "",
                "quantity": quantity_element.text_content() or "0"
            }
            items.append(item_details)
        
        return items
    
    @allure.step("Remove item from cart: {item_name}")
    def remove_item_by_name(self, item_name: str) -> 'CartPage':
        """
        Remove an item from the cart by its name.
        
        Args:
            item_name: Name of the item to remove
            
        Returns:
            CartPage: Self for method chaining
        """
        # Convert item name to data-test format
        data_test_name = item_name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")
        remove_button_selector = f'[data-test="remove-{data_test_name}"]'
        self.click_element(remove_button_selector)
        return self
    
    @allure.step("Continue shopping")
    def continue_shopping(self) -> None:
        """
        Click continue shopping button to go back to inventory.
        """
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        """
        Click checkout button to proceed to checkout.
        """
        self.click_element(self.CHECKOUT_BUTTON)
    
    @allure.step("Check if cart is empty")
    def is_cart_empty(self) -> bool:
        """
        Check if the cart is empty.
        
        Returns:
            True if cart is empty, False otherwise
        """
        return self.get_cart_item_count() == 0
    
    @allure.step("Verify item is in cart: {item_name}")
    def verify_item_in_cart(self, item_name: str) -> bool:
        """
        Verify that a specific item is in the cart.
        
        Args:
            item_name: Name of the item to verify
            
        Returns:
            True if item is in cart, False otherwise
        """
        cart_items = self.get_cart_item_names()
        return item_name in cart_items
    
    @allure.step("Verify item is not in cart: {item_name}")
    def verify_item_not_in_cart(self, item_name: str) -> bool:
        """
        Verify that a specific item is not in the cart.
        
        Args:
            item_name: Name of the item to verify
            
        Returns:
            True if item is not in cart, False otherwise
        """
        cart_items = self.get_cart_item_names()
        return item_name not in cart_items
    
    @allure.step("Calculate total price")
    def calculate_total_price(self) -> float:
        """
        Calculate the total price of all items in the cart.
        
        Returns:
            Total price as float
        """
        prices = self.get_cart_item_prices()
        quantities = self.get_cart_item_quantities()
        
        total = 0.0
        for i, price in enumerate(prices):
            if i < len(quantities):
                # Remove $ and convert to float
                price_value = float(price.replace('$', ''))
                quantity = quantities[i]
                total += price_value * quantity
        
        return total
    
    @allure.step("Get cart badge count")
    def get_cart_badge_count(self) -> int:
        """
        Get the number displayed in the shopping cart badge.
        
        Returns:
            Cart badge count, 0 if no badge visible
        """
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            badge_text = self.get_text(self.SHOPPING_CART_BADGE)
            try:
                return int(badge_text)
            except ValueError:
                return 0
        return 0
    
    def wait_for_cart_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for cart page to be fully loaded.
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        self.wait_for_element(self.PAGE_TITLE, timeout)
        self.wait_for_element(self.CART_CONTENTS_CONTAINER, timeout)