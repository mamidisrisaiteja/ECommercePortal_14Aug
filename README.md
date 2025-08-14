# E-commerce Test Automation Framework

A comprehensive test automation framework built with **Playwright**, **Python**, **pytest-bdd**, and enhanced reporting features. This framework implements the **Page Object Model** design pattern and supports **Behavior Driven Development (BDD)** using Gherkin syntax.

## 🚀 Features

- **Playwright Integration**: Cross-browser testing support (Chromium, Firefox, WebKit)
- **BDD Support**: Gherkin feature files with pytest-bdd
- **Page Object Model**: Maintainable and scalable test architecture
- **Enhanced Reporting**: Allure reports with screenshots, videos, and traces
- **Excel Integration**: Test data management using MCP Excel server
- **Parallel Execution**: Support for parallel test execution
- **Multi-environment Support**: Configurable test environments
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📁 Project Structure

```
ECommercePortal_14Aug/
├── framework/                    # Core framework components
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── pages/                   # Page Object Model classes
│   │   ├── __init__.py
│   │   ├── base_page.py        # Base page class
│   │   ├── login_page.py       # Login page objects
│   │   ├── inventory_page.py   # Inventory page objects
│   │   └── cart_page.py        # Cart page objects
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── browser_manager.py  # Browser lifecycle management
│       ├── data_manager.py     # Excel data handling
│       └── report_manager.py   # Enhanced reporting
├── tests/                      # Test files
│   ├── conftest.py            # Pytest configuration
│   ├── features/              # Gherkin feature files
│   │   ├── authentication.feature
│   │   ├── inventory.feature
│   │   └── cart.feature
│   ├── step_definitions/      # BDD step definitions
│   │   ├── test_authentication_steps.py
│   │   ├── test_inventory_steps.py
│   │   └── test_cart_steps.py
│   ├── test_authentication.py # Authentication tests
│   ├── test_inventory.py     # Inventory tests
│   └── test_cart.py          # Cart tests
├── TestData/                  # Test data files
│   └── TestCaseDocument.xlsx # Excel test case document
├── reports/                   # Generated reports
│   ├── allure-results/       # Allure results
│   ├── screenshots/          # Test screenshots
│   └── videos/              # Test videos
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Poetry configuration
├── run_tests.py            # Test execution script
└── run_tests.bat           # Windows batch script
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js 14+ (for Playwright browsers)
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mamidisrisaiteja/ECommercePortal_14Aug.git
   cd ECommercePortal_14Aug
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

## 🧪 Running Tests

### Quick Start

```bash
# Run all tests
python run_tests.py

# Run specific test suite
pytest tests/test_authentication.py -v

# Run with specific browser
pytest --browser=firefox -v

# Run in parallel
pytest -n 4 -v

# Run with Allure reporting
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### BDD Feature Tests

```bash
# Run authentication features
pytest tests/step_definitions/test_authentication_steps.py::test_valid_login -v

# Run all BDD tests
pytest tests/step_definitions/ -v
```

### Test Configuration

Edit `config.yaml` to customize test settings:

```yaml
base_url: "https://www.saucedemo.com"
timeout: 30000
headless: false
browser: "chromium"
screenshots_dir: "reports/screenshots"
videos_dir: "reports/videos"
```

## 📊 Test Reports

### Allure Reports

Generate comprehensive HTML reports with:

```bash
# Generate and serve Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

Features:
- Test execution timeline
- Screenshots on failure
- Step-by-step execution details
- Test metrics and trends
- Environment information

### HTML Reports

```bash
# Generate simple HTML report
pytest --html=reports/report.html --self-contained-html
```

## 🏗️ Framework Architecture

### Page Object Model

The framework implements the Page Object Model pattern:

- **BasePage**: Common functionality for all pages
- **LoginPage**: Login page specific elements and actions
- **InventoryPage**: Product listing page operations
- **CartPage**: Shopping cart functionality

### BDD Implementation

Using pytest-bdd for behavior-driven development:

```gherkin
Feature: User Authentication
  Scenario: Valid user login
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to the inventory page
```

### Configuration Management

Centralized configuration using:
- YAML configuration files
- Environment variables
- Command-line parameters

## 📋 Test Cases

The framework includes test cases for:

### Authentication (TC_AUTH_01, TC_AUTH_02)
- Valid user login
- Invalid credentials handling
- Error message validation

### Inventory Management (TC_INV_01, TC_INV_02)
- Product listing display
- Add products to cart
- Product information validation

### Shopping Cart (TC_CART_01)
- View cart contents
- Remove items from cart
- Checkout process

## 🔧 MCP Server Integration

This framework leverages Model Context Protocol (MCP) servers:

### Excel MCP Server
- Read test data from Excel files
- Dynamic test case generation
- Data-driven testing support

### Playwright MCP Server
- Enhanced browser automation
- Real-time element inspection
- Cross-browser compatibility testing

## 🚀 CI/CD Integration

### GitHub Actions

Example workflow:

```yaml
name: Test Automation
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run tests
        run: pytest --alluredir=allure-results
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: allure-results
          path: allure-results
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Create an issue in the GitHub repository
- Contact: [Your Email]
- Documentation: [Wiki Link]

## 🏆 Features Showcase

### ✅ Completed Features
- ✅ Page Object Model implementation
- ✅ BDD with Gherkin scenarios
- ✅ Allure reporting integration
- ✅ Excel test data management
- ✅ MCP server integration
- ✅ Cross-browser testing
- ✅ Parallel test execution
- ✅ Screenshot capture on failure
- ✅ Video recording support
- ✅ Multi-environment configuration

### 🔄 Upcoming Features
- 🔄 API testing integration
- 🔄 Mobile testing support
- 🔄 Performance testing
- 🔄 Visual regression testing
- 🔄 Database validation

---

**Built with ❤️ using Playwright, Python, and MCP Servers**