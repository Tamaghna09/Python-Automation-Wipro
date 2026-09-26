import unittest
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.config_reader import ConfigReader
from utilities.csv_reader import CSVReader
from utilities.driver_factory import DriverFactory
from utilities.custom_logger import CustomLogger

@pytest.mark.usefixtures("setup_and_teardown")
class TestSearch(unittest.TestCase):
    """
    Test suite for Product Search functionality.
    Compatible with both PyTest and Python's native Unittest runner.
    """

    driver = None
    logger = CustomLogger.get_logger("TestSearch")

    def setUp(self):
        """Fallback setup when executed directly via Python Unittest runner."""
        if self.driver is None:
            self.driver = DriverFactory.get_driver()
            self.driver.get(ConfigReader.get_base_url())

    def tearDown(self):
        """Fallback teardown when executed directly via Python Unittest runner."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_search_existing_product(self):
        """Verify searching for an existing product displays it in the search results."""
        self.logger.info("=== Starting test_search_existing_product ===")
        home_page = HomePage(self.driver)
        search_results_page = home_page.search_for_product("MacBook")

       
        self.assertTrue(
            search_results_page.is_product_displayed("MacBook"),
            "Expected product 'MacBook' was not found in the search results."
        )
        self.logger.info("=== Finished test_search_existing_product successfully ===")

    @pytest.mark.regression
    def test_search_non_existing_product(self):
        """Verify searching for a non-existing product displays the appropriate message."""
        self.logger.info("=== Starting test_search_non_existing_product ===")
        home_page = HomePage(self.driver)
        search_results_page = home_page.search_for_product("FitbitSmartwatch")

        self.assertTrue(
            search_results_page.is_no_product_message_displayed(),
            "'No product that matches' message was not displayed for non-existing item."
        )

        message_text = search_results_page.get_no_product_message()
        self.assertIn(
            "There is no product that matches the search criteria.",
            message_text,
            f"Unexpected empty search message: {message_text}"
        )
        self.logger.info("=== Finished test_search_non_existing_product successfully ===")

    @pytest.mark.regression
    def test_search_data_driven_csv(self):
        """
        Data-driven test for searching multiple products from test_data/search_data.csv.
        """
        self.logger.info("=== Starting test_search_data_driven_csv ===")
        search_rows = CSVReader.get_data("search_data.csv")

        for row in search_rows:
            product_name, expected_result = row[0], row[1]
            self.logger.info(f"Testing search for product: '{product_name}', expected: '{expected_result}'")

            home_page = HomePage(self.driver)
            search_results_page = home_page.search_for_product(product_name)

            if expected_result == "found":
                self.assertTrue(
                    search_results_page.is_product_displayed(product_name),
                    f"Product '{product_name}' was expected in search results but was missing."
                )
            elif expected_result == "not_found":
                self.assertTrue(
                    search_results_page.is_no_product_message_displayed(),
                    f"No-product message was expected for '{product_name}', but not displayed."
                )

        self.logger.info("=== Finished test_search_data_driven_csv successfully ===")

if __name__ == "__main__":
    unittest.main()