"""
Inventory/Products page object implementing the Page Object Model pattern.
Contains all elements and actions related to the products listing page.
"""

from typing import List, Optional
from playwright.sync_api import Page, Locator
from framework.pages.base_page import BasePage
import allure


class InventoryPage(BasePage):
    """Inventory/Products page object for SauceDemo application."""
    
    # Page elements - MCP verified selectors
    PAGE_TITLE = '[data-test="title"]'  # Confirmed via MCP
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'  # Confirmed via MCP
    INVENTORY_LIST = '[data-test="inventory-list"]'  # Confirmed via MCP
    INVENTORY_ITEM = '[data-test="inventory-item"]'  # Confirmed via MCP
    INVENTORY_ITEM_NAME = '[data-test="inventory-item-name"]'  # Confirmed via MCP
    INVENTORY_ITEM_PRICE = '[data-test="inventory-item-price"]'  # Confirmed via MCP
    INVENTORY_ITEM_IMG = '.inventory_item_img'  # Confirmed via MCP
    INVENTORY_ITEM_DESC = '[data-test="inventory-item-desc"]'  # Confirmed via MCP
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart"]'  # Confirmed via MCP
    REMOVE_BUTTON = '[data-test^="remove"]'  # Confirmed via MCP
    SORT_DROPDOWN = '[data-test="product-sort-container"]'  # Confirmed via MCP
    ACTIVE_OPTION = '[data-test="active-option"]'  # Confirmed via MCP
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'  # Confirmed via MCP
    SHOPPING_CART_BADGE = '.shopping_cart_badge'
    MENU_BUTTON = '#react-burger-menu-btn'  # Confirmed via MCP
    
    # Header elements - MCP verified
    HEADER_CONTAINER = '[data-test="header-container"]'  # Confirmed via MCP
    PRIMARY_HEADER = '[data-test="primary-header"]'  # Confirmed via MCP
    SECONDARY_HEADER = '[data-test="secondary-header"]'  # Confirmed via MCP
    
    # Sort options
    SORT_NAME_A_TO_Z = 'az'
    SORT_NAME_Z_TO_A = 'za'
    SORT_PRICE_LOW_TO_HIGH = 'lohi'
    SORT_PRICE_HIGH_TO_LOW = 'hilo'
    
    def __init__(self, page: Page):
        """
        Initialize the inventory page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.url = f"{self.config.base_url}/inventory.html"
    
    def is_loaded(self) -> bool:
        """
        Check if the inventory page is loaded.
        
        Returns:
            True if inventory page is loaded, False otherwise
        """
        return (self.is_element_visible(self.PAGE_TITLE) and 
                self.is_element_visible(self.INVENTORY_CONTAINER) and
                self.get_text(self.PAGE_TITLE) == "Products")
    
    @allure.step("Verify Products page is displayed")
    def verify_products_page(self) -> bool:
        """
        Verify that the Products page is displayed correctly.
        
        Returns:
            True if Products page is displayed, False otherwise
        """
        return (self.is_element_visible(self.PAGE_TITLE) and 
                "Products" in self.get_text(self.PAGE_TITLE))
    
    @allure.step("Verify Add to cart buttons are present")
    def verify_add_to_cart_buttons(self) -> bool:
        """
        Verify that Add to cart buttons are present on the page.
        
        Returns:
            True if Add to cart buttons are present, False otherwise
        """
        return len(self.page.locator(self.ADD_TO_CART_BUTTON).all()) > 0
    
    @allure.step("Get all product names")
    def get_product_names(self) -> List[str]:
        """
        Get all product names from the inventory.
        
        Returns:
            List of product names
        """
        product_elements = self.page.locator(self.INVENTORY_ITEM_NAME).all()
        return [element.text_content() or "" for element in product_elements]
    
    @allure.step("Get all product prices")
    def get_product_prices(self) -> List[str]:
        """
        Get all product prices from the inventory.
        
        Returns:
            List of product prices
        """
        price_elements = self.page.locator(self.INVENTORY_ITEM_PRICE).all()
        return [element.text_content() or "" for element in price_elements]
    
    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name: str) -> 'InventoryPage':
        """
        Add a specific product to cart by name.
        
        Args:
            product_name: Name of the product to add
            
        Returns:
            Self for method chaining
        """
        # Convert product name to data-test attribute format
        test_id = product_name.lower().replace(' ', '-').replace("'", "")
        add_button_selector = f'[data-test="add-to-cart-{test_id}"]'
        
        self.click_element(add_button_selector)
        return self
    
    @allure.step("Remove product from cart: {product_name}")
    def remove_product_from_cart(self, product_name: str) -> 'InventoryPage':
        """
        Remove a specific product from cart by name.
        
        Args:
            product_name: Name of the product to remove
            
        Returns:
            Self for method chaining
        """
        # Convert product name to data-test attribute format
        test_id = product_name.lower().replace(' ', '-').replace("'", "")
        remove_button_selector = f'[data-test="remove-{test_id}"]'
        
        self.click_element(remove_button_selector)
        return self
    
    @allure.step("Sort products by: {sort_option}")
    def sort_products(self, sort_option: str) -> 'InventoryPage':
        """
        Sort products by the specified option.
        
        Args:
            sort_option: Sort option (az, za, lohi, hilo)
            
        Returns:
            Self for method chaining
        """
        self.select_dropdown_option(self.SORT_DROPDOWN, sort_option)
        return self
    
    @allure.step("Sort products by Name (A to Z)")
    def sort_by_name_a_to_z(self) -> 'InventoryPage':
        """
        Sort products by name from A to Z.
        
        Returns:
            Self for method chaining
        """
        return self.sort_products(self.SORT_NAME_A_TO_Z)
    
    @allure.step("Sort products by Name (Z to A)")
    def sort_by_name_z_to_a(self) -> 'InventoryPage':
        """
        Sort products by name from Z to A.
        
        Returns:
            Self for method chaining
        """
        return self.sort_products(self.SORT_NAME_Z_TO_A)
    
    @allure.step("Sort products by Price (Low to High)")
    def sort_by_price_low_to_high(self) -> 'InventoryPage':
        """
        Sort products by price from low to high.
        
        Returns:
            Self for method chaining
        """
        return self.sort_products(self.SORT_PRICE_LOW_TO_HIGH)
    
    @allure.step("Sort products by Price (High to Low)")
    def sort_by_price_high_to_low(self) -> 'InventoryPage':
        """
        Sort products by price from high to low.
        
        Returns:
            Self for method chaining
        """
        return self.sort_products(self.SORT_PRICE_HIGH_TO_LOW)
    
    def verify_products_sorted_alphabetically(self, ascending: bool = True) -> bool:
        """
        Verify that products are sorted alphabetically.
        
        Args:
            ascending: True for A-Z, False for Z-A
            
        Returns:
            True if products are sorted correctly, False otherwise
        """
        product_names = self.get_product_names()
        sorted_names = sorted(product_names) if ascending else sorted(product_names, reverse=True)
        return product_names == sorted_names
    
    def verify_products_sorted_by_price(self, ascending: bool = True) -> bool:
        """
        Verify that products are sorted by price.
        
        Args:
            ascending: True for low to high, False for high to low
            
        Returns:
            True if products are sorted correctly, False otherwise
        """
        prices = self.get_product_prices()
        # Convert prices to float for comparison (remove $ sign)
        price_values = [float(price.replace('$', '')) for price in prices]
        sorted_prices = sorted(price_values) if ascending else sorted(price_values, reverse=True)
        return price_values == sorted_prices
    
    @allure.step("Click shopping cart")
    def click_shopping_cart(self) -> None:
        """Click on the shopping cart link."""
        self.click_element(self.SHOPPING_CART_LINK)
    
    def get_cart_badge_count(self) -> int:
        """
        Get the number displayed on the shopping cart badge.
        
        Returns:
            Number of items in cart, 0 if no badge is visible
        """
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            badge_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(badge_text) if badge_text.isdigit() else 0
        return 0
    
    def get_inventory_item_count(self) -> int:
        """
        Get the total number of inventory items displayed.
        
        Returns:
            Number of inventory items
        """
        return len(self.page.locator(self.INVENTORY_ITEM).all())
    
    @allure.step("Click on product: {product_name}")
    def click_product(self, product_name: str) -> None:
        """
        Click on a specific product to view details.
        
        Args:
            product_name: Name of the product to click
        """
        product_locator = self.page.locator(self.INVENTORY_ITEM_NAME).filter(has_text=product_name)
        product_locator.click()
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if a product is already added to cart (Remove button is visible).
        
        Args:
            product_name: Name of the product to check
            
        Returns:
            True if product is in cart, False otherwise
        """
        test_id = product_name.lower().replace(' ', '-').replace("'", "")
        remove_button_selector = f'[data-test="remove-{test_id}"]'
        return self.is_element_visible(remove_button_selector)