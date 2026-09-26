from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AccountPage(BasePage):
    """Page Object for Authenticated User Account Dashboard."""

    # Locators
    MY_ACCOUNT_HEADER = (By.XPATH, "//h2[normalize-space()='My Account']")
    EDIT_ACCOUNT_LINK = (By.LINK_TEXT, "Edit your account information")
    LOGOUT_LINK = (By.XPATH, "//aside[@id='column-right']//a[normalize-space()='Logout']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_user_logged_in(self):
        """Validates if 'My Account' heading or 'Edit your account information' link is visible."""
        return self.is_element_displayed(self.MY_ACCOUNT_HEADER) or self.is_element_displayed(self.EDIT_ACCOUNT_LINK)

    def click_logout(self):
        """Logs out from the user session."""
        self.logger.info("Logging out user")
        self.do_click(self.LOGOUT_LINK)