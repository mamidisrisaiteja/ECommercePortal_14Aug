"""
Login page object implementing the Page Object Model pattern.
Contains all elements and actions related to the login page.
"""

from typing import Optional
from playwright.sync_api import Page
from framework.pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Login page object for SauceDemo application."""
    
    # Page elements - Based on actual MCP inspection
    USERNAME_INPUT = '[data-test="username"]'  # Confirmed via MCP
    PASSWORD_INPUT = '[data-test="password"]'  # Confirmed via MCP
    LOGIN_BUTTON = '[data-test="login-button"]'  # Confirmed via MCP
    ERROR_MESSAGE = '.error-message-container'  # Updated from MCP inspection
    ERROR_BUTTON = '.error-button'
    LOGIN_LOGO = '.login_logo'  # Confirmed via MCP
    LOGIN_CONTAINER = '[data-test="login-container"]'  # Found via MCP
    LOGIN_CREDENTIALS = '[data-test="login-credentials"]'  # Found via MCP
    
    def __init__(self, page: Page):
        """
        Initialize the login page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)
        self.url = f"{self.config.base_url}/"
    
    def is_loaded(self) -> bool:
        """
        Check if the login page is loaded.
        
        Returns:
            True if login page is loaded, False otherwise
        """
        return (self.is_element_visible(self.LOGIN_LOGO) and 
                self.is_element_visible(self.USERNAME_INPUT) and
                self.is_element_visible(self.PASSWORD_INPUT) and
                self.is_element_visible(self.LOGIN_BUTTON))
    
    @allure.step("Navigate to login page")
    def navigate(self) -> 'LoginPage':
        """
        Navigate to the login page.
        
        Returns:
            LoginPage: Self for method chaining
        """
        self.navigate_to(self.url)
        return self
    
    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username in the username field.
        
        Args:
            username: Username to enter
            
        Returns:
            LoginPage: Self for method chaining
        """
        self.fill_text(self.USERNAME_INPUT, username)
        return self
    
    @allure.step("Enter password")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter
            
        Returns:
            LoginPage: Self for method chaining
        """
        self.fill_text(self.PASSWORD_INPUT, password)
        return self
    
    @allure.step("Click login button")
    def click_login(self) -> None:
        """
        Click the login button.
        """
        self.click_element(self.LOGIN_BUTTON)
    
    @allure.step("Login with credentials: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    @allure.step("Login with standard user")
    def login_standard_user(self) -> None:
        """
        Login with standard user credentials from config.
        """
        self.login(self.config.standard_user, self.config.standard_password)
    
    @allure.step("Login with locked user")
    def login_locked_user(self) -> None:
        """
        Login with locked user credentials from config.
        """
        self.login(self.config.locked_user, self.config.standard_password)
    
    @allure.step("Login with problem user")
    def login_problem_user(self) -> None:
        """
        Login with problem user credentials from config.
        """
        self.login(self.config.problem_user, self.config.standard_password)
    
    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """
        Get the error message text.
        
        Returns:
            Error message text
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    @allure.step("Check if error message is displayed")
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    @allure.step("Clear error message")
    def clear_error_message(self) -> 'LoginPage':
        """
        Clear the error message by clicking the X button.
        
        Returns:
            LoginPage: Self for method chaining
        """
        if self.is_element_visible(self.ERROR_BUTTON):
            self.click_element(self.ERROR_BUTTON)
        return self
    
    @allure.step("Get login logo text")
    def get_login_logo_text(self) -> str:
        """
        Get the login logo text.
        
        Returns:
            Logo text
        """
        return self.get_text(self.LOGIN_LOGO)
    
    @allure.step("Check if login credentials section is visible")
    def is_login_credentials_visible(self) -> bool:
        """
        Check if login credentials section is visible.
        
        Returns:
            True if credentials section is visible, False otherwise
        """
        return self.is_element_visible(self.LOGIN_CREDENTIALS)
    
    @allure.step("Get available usernames from credentials section")
    def get_available_usernames(self) -> list:
        """
        Get list of available usernames from the credentials section.
        
        Returns:
            List of available usernames
        """
        if self.is_login_credentials_visible():
            credentials_text = self.get_text(self.LOGIN_CREDENTIALS)
            # Parse usernames from the credentials text
            # This is specific to SauceDemo format
            lines = credentials_text.split('\n')
            usernames = []
            for line in lines:
                if 'user' in line.lower() and '_user' in line:
                    # Extract username from line
                    words = line.split()
                    for word in words:
                        if '_user' in word:
                            usernames.append(word)
            return usernames
        return []
    
    def wait_for_login_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for login page to be fully loaded.
        
        Args:
            timeout: Optional timeout in milliseconds
        """
        self.wait_for_element(self.LOGIN_LOGO, timeout)
        self.wait_for_element(self.USERNAME_INPUT, timeout)
        self.wait_for_element(self.PASSWORD_INPUT, timeout)
        self.wait_for_element(self.LOGIN_BUTTON, timeout)