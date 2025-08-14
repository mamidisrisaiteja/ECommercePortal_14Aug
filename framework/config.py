"""
Configuration module for the test automation framework.
Loads settings from environment variables and provides configuration management.
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config(BaseSettings):
    """Configuration class using Pydantic for validation and type safety."""
    
    # Application settings
    base_url: str = Field(default="https://www.saucedemo.com", env="BASE_URL")
    
    # Browser settings  
    browser: str = Field(default="chromium", env="BROWSER")
    headless: bool = Field(default=False, env="HEADLESS")
    viewport_width: int = Field(default=1280, env="VIEWPORT_WIDTH")
    viewport_height: int = Field(default=720, env="VIEWPORT_HEIGHT")
    
    # Test settings
    timeout: int = Field(default=30000, env="TIMEOUT")
    retry_count: int = Field(default=2, env="RETRY_COUNT")
    parallel_workers: int = Field(default=4, env="PARALLEL_WORKERS")
    
    # Credentials
    standard_user: str = Field(default="standard_user", env="STANDARD_USER")
    standard_password: str = Field(default="secret_sauce", env="STANDARD_PASSWORD")
    locked_user: str = Field(default="locked_out_user", env="LOCKED_USER")
    problem_user: str = Field(default="problem_user", env="PROBLEM_USER")
    performance_user: str = Field(default="performance_glitch_user", env="PERFORMANCE_USER")
    
    # Reporting paths
    allure_results_dir: str = Field(default="reports/allure-results", env="ALLURE_RESULTS_DIR")
    html_report_path: str = Field(default="reports/report.html", env="HTML_REPORT_PATH")
    screenshots_dir: str = Field(default="reports/screenshots", env="SCREENSHOTS_DIR")
    videos_dir: str = Field(default="reports/videos", env="VIDEOS_DIR")
    
    # Test data
    excel_file_path: str = Field(default="TestData/TestCaseDocument.xlsx", env="EXCEL_FILE_PATH")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global configuration instance
_config = None


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config: The configuration object
    """
    global _config
    if _config is None:
        _config = Config()
        
        # Ensure directories exist
        os.makedirs(_config.allure_results_dir, exist_ok=True)
        os.makedirs(_config.screenshots_dir, exist_ok=True)
        os.makedirs(_config.videos_dir, exist_ok=True)
        os.makedirs(os.path.dirname(_config.html_report_path), exist_ok=True)
        
    return _config


def get_browser_config() -> dict:
    """
    Get browser-specific configuration.
    
    Returns:
        dict: Browser configuration settings
    """
    config = get_config()
    return {
        "browser": config.browser,
        "headless": config.headless,
        "viewport": {
            "width": config.viewport_width,
            "height": config.viewport_height
        },
        "timeout": config.timeout
    }


def get_user_credentials(user_type: str = "standard") -> dict:
    """
    Get user credentials based on user type.
    
    Args:
        user_type: Type of user (standard, locked, problem, performance)
        
    Returns:
        dict: User credentials
    """
    config = get_config()
    
    credentials_map = {
        "standard": {"username": config.standard_user, "password": config.standard_password},
        "locked": {"username": config.locked_user, "password": config.standard_password},
        "problem": {"username": config.problem_user, "password": config.standard_password},
        "performance": {"username": config.performance_user, "password": config.standard_password}
    }
    
    return credentials_map.get(user_type, credentials_map["standard"])