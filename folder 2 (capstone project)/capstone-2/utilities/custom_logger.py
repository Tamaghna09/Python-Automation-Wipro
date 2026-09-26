import logging
import os

class CustomLogger:
    """Utility class to set up centralized, formatted logging for test execution."""

    @staticmethod
    def get_logger(name=__name__):
        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(logging.INFO)

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(base_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)

            log_file_path = os.path.join(logs_dir, "automation.log")

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | [%(name)s] : %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # File handler
            file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            logger.addHandler(console_handler)

        return logger