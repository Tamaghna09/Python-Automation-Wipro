import csv
import os

class CSVReader:
    """Utility class to read tabular test data from CSV files."""

    @staticmethod
    def get_data(file_name):
        """
        Reads CSV file and returns rows as a list of lists (excluding header).
        :param file_name: File name in test_data folder (e.g., 'login_data.csv')
        :return: list of rows [ [col1, col2, ...], ... ]
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "test_data", file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found at: {file_path}")

        rows = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                if row:  # skip blank lines
                    rows.append(row)
        return rows

    @staticmethod
    def get_data_as_dict(file_name):
        """
        Reads CSV file and returns rows as a list of dictionaries with header keys.
        :param file_name: File name in test_data folder
        :return: list of dicts [ {col_name: val}, ... ]
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "test_data", file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found at: {file_path}")

        rows = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return rows