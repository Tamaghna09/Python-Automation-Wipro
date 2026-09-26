import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

class BasePage:
    """
    BasePage serves as the parent class for all Page Objects.
    Encapsulates core Selenium actions with robust explicit waits.
    """

    def __init__(self, driver):
        self.driver = driver
        self.timeout = ConfigReader.get_explicit_wait()
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger = CustomLogger.get_logger(self.__class__.__name__)

    def do_click(self, locator):
       
        try:
            self.logger.info(f"Clicking element: {locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}. Error: {str(e)}")
            raise

    def do_send_keys(self, locator, text):
        """Waits until an element is visible, clears existing text, and enters new text."""
        try:
            self.logger.info(f"Typing into element: {locator}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to send keys to element: {locator}. Error: {str(e)}")
            raise

    def get_element_text(self, locator):
        """Waits until an element is visible and returns its text."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text.strip()
            self.logger.info(f"Retrieved text '{text}' from element: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to retrieve text from element: {locator}. Error: {str(e)}")
            raise

    def is_element_displayed(self, locator):
        """Checks if an element is visible within the timeout."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False

    def get_page_title(self):
        """Returns current page title."""
        title = self.driver.title
        self.logger.info(f"Current page title: '{title}'")
        return title

    def get_current_url(self):
        """Returns current page URL."""
        return self.driver.current_url

    def capture_screenshot(self, name_prefix="screenshot"):
        """Captures screenshot and stores it inside the screenshots/ directory."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshots_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{name_prefix}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)

        self.driver.save_screenshot(file_path)
        self.logger.info(f"Screenshot saved at: {file_path}")
        return file_path