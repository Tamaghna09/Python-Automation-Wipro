import configparser
import os

class ConfigReader:
    """Utility class to read framework configuration parameters from config.ini."""

    _config = None

    @classmethod
    def _load_config(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "configurations", "config.ini")
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Configuration file not found at: {config_path}")
            cls._config.read(config_path)

    @classmethod
    def get_value(cls, section, key):
        cls._load_config()
        return cls._config.get(section, key)

    @classmethod
    def get_base_url(cls):
        return cls.get_value("common", "base_url")

    @classmethod
    def get_browser(cls):
        return cls.get_value("common", "browser")

    @classmethod
    def get_implicit_wait(cls):
        return int(cls.get_value("common", "implicit_wait"))

    @classmethod
    def get_explicit_wait(cls):
        return int(cls.get_value("common", "explicit_wait"))

    @classmethod
    def is_headless(cls):
        return cls.get_value("common", "headless").strip().lower() in ("true", "1", "yes")