# Capstone Assignment 2: Selenium Python Automation Framework (Unittest + PyTest + POM)

An enterprise-grade, scalable Test Automation Framework built with **Selenium WebDriver (Python)**, **PyTest**, and **Unittest**, following the **Page Object Model (POM)** architectural design pattern.

---

## 📌 Project Highlights & Capstone Objectives
- **Target Application**: [TutorialsNinja Demo](https://tutorialsninja.com/demo/)
- **Core Scenarios**: E-Commerce **Login** & **Product Search**
- **Design Pattern**: Page Object Model (POM) separating locators, page actions, and test assertions.
- **Dual Test Runners**: Full support for both **PyTest** and Python **Unittest**.
- **Configuration Management**: Centralized `configurations/config.ini` parsed via `ConfigReader`.
- **Data-Driven Testing (DDT)**: External CSV datasets (`login_data.csv`, `search_data.csv`) handled via `CSVReader`.
- **Failure Diagnostics**: Automated screenshot capture on failed assertions, embedded into **PyTest HTML Reports**.
- **Logging**: Timestamped file and console logging via `CustomLogger` into `logs/automation.log`.

---

## 📁 Project Structure

```text
selenium_ecommerce_framework/
│
├── configurations/
│   └── config.ini                 # Base URL, browser name, timeouts, headless flag
│
├── test_data/
│   ├── login_data.csv             # Test credentials for data-driven login tests
│   └── search_data.csv            # Test search keywords & expected outcomes
│
├── utilities/
│   ├── __init__.py
│   ├── config_reader.py           # Reads config.ini properties
│   ├── csv_reader.py              # Parses CSV files into test lists/dicts
│   ├── custom_logger.py           # Logging configuration (console + log file)
│   └── driver_factory.py          # Multi-browser driver initialization (Chrome, Firefox, Edge)
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py               # Reusable explicit wait wrapper methods & screenshot
│   ├── home_page.py               # Homepage locators and action methods
│   ├── login_page.py              # Login form locators and verification methods
│   ├── account_page.py            # Post-login user dashboard page object
│   └── search_results_page.py     # Product search grid and result verifications
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Fixtures, browser hooks, screenshot-on-failure
│   ├── test_login.py              # Login test cases (positive, negative, blank)
│   └── test_search.py             # Product search test cases (positive, negative, CSV)
│
├── reports/                       # Generated HTML execution reports (report.html)
├── screenshots/                   # Failure screenshots saved with timestamps
├── logs/                          # Runtime logs (logs/automation.log)
│
├── pytest.ini                     # PyTest configurations, markers, default CLI flags
├── requirements.txt               # Project dependencies
├── test_runner_unittest.py        # Unittest TestSuite runner script
└── README.md                      # Documentation & viva preparation guide