import unittest
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utilities.config_reader import ConfigReader
from utilities.csv_reader import CSVReader
from utilities.driver_factory import DriverFactory
from utilities.custom_logger import CustomLogger

@pytest.mark.usefixtures("setup_and_teardown")
class TestLogin(unittest.TestCase):
    """
    Test suite for Login functionality.
    Compatible with both PyTest and Python's native Unittest runner.
    """

    driver = None
    logger = CustomLogger.get_logger("TestLogin")

    def setUp(self):
        """Fallback setup when executed directly via Python Unittest runner."""
        if self.driver is None:
            self.driver = DriverFactory.get_driver()
            self.driver.get(ConfigReader.get_base_url())

    def tearDown(self):
        """Fallback teardown when executed directly via Python Unittest runner."""
        if not hasattr(self, "_pytestfixturefunction"):
            if self.driver:
                self.driver.quit()
                self.driver = None

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_valid_login(self):
        """Verify that a user can successfully log in with valid credentials."""
        self.logger.info("=== Starting test_valid_login ===")
        home_page = HomePage(self.driver)
        login_page = home_page.navigate_to_login()

        # Execute login
        account_page = login_page.login("amotooricap9@gmail.com", "12345")

        # Assertion
        self.assertTrue(
            account_page.is_user_logged_in(),
            "User failed to log in with valid credentials; Account page not displayed."
        )
        self.logger.info("=== Finished test_valid_login successfully ===")

    @pytest.mark.regression
    def test_invalid_login_data_driven(self):
        """
        Data-driven test for invalid login attempts using test_data/login_data.csv.
        Validates that appropriate warning banner is displayed.
        """
        self.logger.info("=== Starting test_invalid_login_data_driven ===")
        test_rows = CSVReader.get_data("login_data.csv")

        for row in test_rows:
            email, password, expected_status = row[0], row[1], row[2]

            if expected_status == "failure":
                self.logger.info(f"Testing invalid login for email: '{email}'")
                home_page = HomePage(self.driver)
                login_page = home_page.navigate_to_login()

                login_page.login(email, password)

                self.assertTrue(
                    login_page.is_warning_displayed(),
                    f"Warning banner not displayed for invalid credentials: {email}"
                )

                warning_text = login_page.get_warning_message()
                self.assertIn(
                    "Warning: No match for E-Mail Address and/or Password.",
                    warning_text,
                    f"Unexpected warning message received: {warning_text}"
                )

        self.logger.info("=== Finished test_invalid_login_data_driven successfully ===")

    @pytest.mark.regression
    def test_login_without_credentials(self):
        """Verify that attempting to log in without entering email/password displays warning banner."""
        self.logger.info("=== Starting test_login_without_credentials ===")
        home_page = HomePage(self.driver)
        login_page = home_page.navigate_to_login()

        login_page.click_login()

        self.assertTrue(
            login_page.is_warning_displayed(),
            "Warning banner not displayed when submitting blank login form."
        )
        self.logger.info("=== Finished test_login_without_credentials successfully ===")

if __name__ == "__main__":
    unittest.main()