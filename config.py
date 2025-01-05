# config.py

import os
import configparser

chrome_user_data_path = os.environ.get("CHROME_USER_DATA")

config = configparser.ConfigParser()
config_path = os.environ.get("CONFIG_PATH")
if not config_path:
    raise ValueError("CONFIG_PATH environment variable is not set.")
config.read(config_path)

# Load Credentials: (First from .env, else from config)
linkedin_username = os.environ.get("LINKEDIN_USERNAME")
if not linkedin_username:
    linkedin_username = config.get("user_info", "username")
    if not linkedin_username:
        raise ValueError("LINKEDIN_USERNAME is not set in environment variables or config.ini.")

linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
if not linkedin_password:
    linkedin_password = config.get("user_info", "password")
    if not linkedin_password:
        raise ValueError("LINKEDIN_PASSWORD is not set in environment variables or config.ini.")

# ... other configuration ...
keywords = config.get("search", "keywords")
location = config.get("search", "location")
time_ago = int(config.get("search", "old", fallback=0))
matching_method = config.get("matching", "method", fallback="fuzz").lower()
threshold = int(config.get("matching", "threshold", fallback=80))
user_description = config.get("matching", "description")
output_file_name = config.get("general", "output_path")

# logging configuration
log_level = config.get("general", "log_level", fallback="DEBUG")
log_file_path = config.get("general", "log_file", fallback=None)
import src.logger as LOGGER
if log_file_path: LOGGER.set_output_path(log_file_path)