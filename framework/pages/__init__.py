"""
Page objects package.
Contains all page object model classes.
"""

from framework.pages.base_page import BasePage
from framework.pages.login_page import LoginPage
from framework.pages.inventory_page import InventoryPage
from framework.pages.cart_page import CartPage

__all__ = [
    "BasePage",
    "LoginPage", 
    "InventoryPage",
    "CartPage"
]