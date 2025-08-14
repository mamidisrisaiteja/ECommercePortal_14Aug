"""
Base page class implementing the Page Object Model pattern.
Provides common functionality for all page objects.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any
from playwright.sync_api import Page, Locator, expect
from framework.config import get_config
import allure
import time


class BasePage(ABC):
    """Base class for all page objects implementing common functionality."""
    
    def __init__(self, page: Page):
        """
        Initialize the base page.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.config = get_config()
        self.timeout = self.config.timeout
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Abstract method to check if the page is loaded.
        Must be implemented by all page classes.
        
        Returns:
            True if page is loaded, False otherwise
        """
        pass
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)
            self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for the page to load completely.
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """
        Wait for an element to be visible.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator object for the element
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator
    
    def click_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click on an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        with allure.step(f"Click element: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.click()
    
    def fill_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Fill text in an input field.
        
        Args:
            selector: CSS selector for the input field
            text: Text to fill
            timeout: Optional timeout in milliseconds
        """
        with allure.step(f"Fill text '{text}' in element: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.clear()
            element.fill(text)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
            
        Returns:
            Text content of the element
        """
        element = self.wait_for_element(selector, timeout)
        return element.text_content() or ""
    
    def is_element_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            timeout = timeout or 5000  # Shorter timeout for visibility checks
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_element_present(self, selector: str) -> bool:
        """
        Check if an element is present in the DOM.
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            True if element is present, False otherwise
        """
        return self.page.locator(selector).count() > 0
    
    def wait_for_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Wait for an element to contain specific text.
        
        Args:
            selector: CSS selector for the element
            text: Text to wait for
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or self.timeout
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)
    
    def select_dropdown_option(self, selector: str, option: str, timeout: Optional[int] = None) -> None:
        """
        Select an option from a dropdown.
        
        Args:
            selector: CSS selector for the dropdown
            option: Option to select
            timeout: Optional timeout in milliseconds
        """
        with allure.step(f"Select option '{option}' from dropdown: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.select_option(option)
    
    def hover_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        with allure.step(f"Hover over element: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.hover()
    
    def scroll_to_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Scroll to an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        with allure.step(f"Scroll to element: {selector}"):
            element = self.wait_for_element(selector, timeout)
            element.scroll_into_view_if_needed()
    
    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            name: Optional name for the screenshot
            
        Returns:
            Path to the screenshot file
        """
        if name is None:
            name = f"screenshot_{int(time.time())}"
        
        screenshot_path = f"{self.config.screenshots_dir}/{name}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        
        # Attach to Allure report
        allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
        
        return screenshot_path
    
    def get_page_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            Page title
        """
        return self.page.title()
    
    def get_current_url(self) -> str:
        """
        Get the current URL.
        
        Returns:
            Current URL
        """
        return self.page.url
    
    def refresh_page(self) -> None:
        """Refresh the current page."""
        with allure.step("Refresh page"):
            self.page.reload()
            self.wait_for_page_load()
    
    def go_back(self) -> None:
        """Navigate back in browser history."""
        with allure.step("Navigate back"):
            self.page.go_back()
            self.wait_for_page_load()
    
    def accept_alert(self) -> None:
        """Accept browser alert/confirm dialog."""
        with allure.step("Accept alert"):
            self.page.on("dialog", lambda dialog: dialog.accept())