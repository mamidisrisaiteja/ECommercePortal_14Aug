"""
Framework package initialization.
Provides easy access to core framework components.
"""

from framework.config import get_config, get_browser_config, get_user_credentials
from framework.utils.browser_manager import get_browser_manager, create_browser_for_test, cleanup_browser
from framework.utils.data_manager import get_test_data_manager, load_all_test_cases, get_credentials_for_test
from framework.utils.report_manager import get_report_manager, log_test_step, attach_screenshot_to_report

# Framework version
__version__ = "1.0.0"

# Export main components
__all__ = [
    "get_config",
    "get_browser_config", 
    "get_user_credentials",
    "get_browser_manager",
    "create_browser_for_test",
    "cleanup_browser",
    "get_test_data_manager",
    "load_all_test_cases",
    "get_credentials_for_test",
    "get_report_manager",
    "log_test_step",
    "attach_screenshot_to_report"
]