from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utilities.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

class DriverFactory:
    """Factory class to instantiate WebDriver instances across multiple browsers."""

    logger = CustomLogger.get_logger("DriverFactory")

    @classmethod
    def get_driver(cls, browser_name=None, headless=None):
        if browser_name is None:
            browser_name = ConfigReader.get_browser()

        if headless is None:
            headless = ConfigReader.is_headless()

        browser = browser_name.lower().strip()
        cls.logger.info(f"Initializing WebDriver for browser: '{browser}' (Headless={headless})")

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()

        elif browser in ("edge", "msedge"):
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(options=options)

        else:
            cls.logger.error(f"Unsupported browser specified: '{browser_name}'. Defaulting to Chrome.")
            options = ChromeOptions()
            driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(ConfigReader.get_implicit_wait())
        return driver