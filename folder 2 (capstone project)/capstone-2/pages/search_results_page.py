from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    """Page Object for Product Search Results Page."""

    # Locators
    PRODUCT_TITLES = (By.CSS_SELECTOR, "div.product-layout div.caption h4 a")
    NO_PRODUCT_MESSAGE = (By.XPATH, "//p[contains(text(),'There is no product that matches the search criteria.')]")
    SEARCH_HEADING = (By.XPATH, "//div[@id='content']/h1[contains(.,'Search')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_product_displayed(self, product_name):
        """Checks if at least one returned product title matches the searched product name."""
        try:
            self.wait.until(lambda d: len(d.find_elements(*self.PRODUCT_TITLES)) > 0)
            product_elements = self.driver.find_elements(*self.PRODUCT_TITLES)
            for elem in product_elements:
                if product_name.lower() in elem.text.strip().lower():
                    self.logger.info(f"Found matching product in search results: '{elem.text}'")
                    return True
            return False
        except Exception:
            return False

    def get_no_product_message(self):
        """Returns the text message displayed when no products match."""
        return self.get_element_text(self.NO_PRODUCT_MESSAGE)

    def is_no_product_message_displayed(self):
        """Checks if the 'no product that matches' message is visible."""
        return self.is_element_displayed(self.NO_PRODUCT_MESSAGE)