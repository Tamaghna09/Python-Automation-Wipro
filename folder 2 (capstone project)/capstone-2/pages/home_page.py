from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for TutorialsNinja Home Page."""

    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MY_ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, "a[title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGO = (By.CSS_SELECTOR, "#logo a")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login(self):
        """Clicks 'My Account' dropdown and selects 'Login'."""
        self.logger.info("Navigating to Login page from Home page")
        self.do_click(self.MY_ACCOUNT_DROPDOWN)
        self.do_click(self.LOGIN_LINK)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def search_for_product(self, product_name):
        """Types product name into search box and clicks the search button."""
        self.logger.info(f"Searching for product: '{product_name}'")
        self.do_send_keys(self.SEARCH_INPUT, product_name)
        self.do_click(self.SEARCH_BUTTON)
        from pages.search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)

    def is_logo_displayed(self):
        """Checks if the store logo is displayed on the homepage."""
        return self.is_element_displayed(self.LOGO)