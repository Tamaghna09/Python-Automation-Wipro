from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.account_page import AccountPage

class LoginPage(BasePage):
    """Page Object for TutorialsNinja Login Page."""

    # Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    WARNING_ALERT = (By.CSS_SELECTOR, "div.alert-danger")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_email(self, email):
        self.do_send_keys(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.do_send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.do_click(self.LOGIN_BUTTON)

    def login(self, email, password):
        """Executes full login sequence and returns AccountPage."""
        self.logger.info(f"Attempting login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return AccountPage(self.driver)

    def get_warning_message(self):
        """Retrieves text from warning alert banner on failed login."""
        return self.get_element_text(self.WARNING_ALERT)

    def is_warning_displayed(self):
        """Checks if warning banner is displayed."""
        return self.is_element_displayed(self.WARNING_ALERT)