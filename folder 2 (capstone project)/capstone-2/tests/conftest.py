import os
from datetime import datetime
import pytest
from utilities.driver_factory import DriverFactory
from utilities.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("Conftest")

def pytest_addoption(parser):
    """Adds custom command-line options for pytest execution."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Target browser: chrome, firefox, or edge"
    )

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown(request):
    """
    Initializes WebDriver instance before each test, navigates to base_url,
    attaches driver to test class, and closes the browser after test execution.
    """
    cmd_browser = request.config.getoption("--browser")
    driver = DriverFactory.get_driver(browser_name=cmd_browser)

    base_url = ConfigReader.get_base_url()
    logger.info(f"Opening Base URL: {base_url}")
    driver.get(base_url)

    # Attach driver to test class instance (for Unittest / class-based tests)
    if request.cls is not None:
        request.cls.driver = driver

    yield driver

    logger.info("Tearing down WebDriver session")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    PyTest hook: Automatically captures a screenshot on test failure
    and embeds it into the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        if "setup_and_teardown" in item.funcargs:
            driver = item.funcargs["setup_and_teardown"]
        elif hasattr(item.instance, "driver"):
            driver = item.instance.driver

        if driver is not None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            screenshots_dir = os.path.join(base_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/", "_").replace(":", "_").replace("[", "_").replace("]", "_")
            file_name = f"FAIL_{test_name}_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)

            driver.save_screenshot(file_path)
            logger.info(f"[FAILURE HOOK] Captured failure screenshot: {file_path}")

            # Attach to pytest-html report
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html is not None:
                extra = getattr(report, "extra", [])
                html_snippet = f'<div><img src="../screenshots/{file_name}" alt="failure screenshot" style="width:300px;height:auto;border:1px solid #d9534f;" onclick="window.open(this.src)" /></div>'
                extra.append(pytest_html.extras.html(html_snippet))
                report.extra = extra