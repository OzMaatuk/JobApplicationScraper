# config.py

import os
import configparser
import src.logger as LOGGER

config = configparser.ConfigParser()
config.read("config.ini")

chrome_user_data_path = os.environ.get("CHROME_USER_DATA")
if not chrome_user_data_path:
    raise ValueError("CHROME_USER_DATA environment variable is not set.")
config.get("general", "user_data_path")

# Load Credentials: (First from .env, else from config)
linkedin_username = os.environ.get("LINKEDIN_USERNAME")
if not linkedin_username:
    linkedin_username = config.get("user_info", "username")
    if not linkedin_username and not chrome_user_data_path:
        raise ValueError("LINKEDIN_USERNAME is not set in environment variables or config.ini.")

linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
if not linkedin_password:
    linkedin_password = config.get("user_info", "password")
    if not linkedin_password and not chrome_user_data_path:
        raise ValueError("LINKEDIN_PASSWORD is not set in environment variables or config.ini.")

# Load resume path
resume_path = config.get("general", "resume_path")
if not resume_path:
    raise ValueError("Resume path is not set in config.ini.")

# ... other configuration ...
keywords = config.get("search", "keywords")
location = config.get("search", "location")
epoch_ago = int(config.get("search", "epoch_ago", fallback="Past 24 hours"))
matching_method = config.get("matching", "method", fallback="fuzz").lower()
threshold = int(config.get("matching", "threshold", fallback=80))
user_description = config.get("matching", "description")
output_file_name = config.get("general", "output_path")

# logging configuration
log_level = config.get("general", "log_level", fallback="DEBUG")
log_file_path = config.get("general", "log_file", fallback=None)
if log_file_path:
    LOGGER.set_output_path(log_file_path)