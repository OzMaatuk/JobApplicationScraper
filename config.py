# config.py

import os
import configparser
import src.logger as LOGGER
from src.constants.constants import Constants

config = configparser.ConfigParser()
config.read("config.ini")

chrome_user_data_path = os.environ.get("CHROME_USER_DATA")
if not chrome_user_data_path:
    raise ValueError("CHROME_USER_DATA environment variable is not set.")
config.get("general", "user_data_path")

# Load Credentials: (First from .env, else from config)
linkedin_username = os.environ.get("LINKEDIN_USERNAME")
if not linkedin_username:
    linkedin_username = config.get("user_info", "username", fallback=None)
    if not linkedin_username:
        raise ValueError("LINKEDIN_USERNAME is not set in environment variables or config.ini.")

linkedin_password = os.environ.get("LINKEDIN_PASSWORD")
if not linkedin_password:
    linkedin_password = config.get("user_info", "password", fallback=None)
    if not linkedin_password:
        raise ValueError("LINKEDIN_PASSWORD is not set in environment variables or config.ini.")

# Load resume path
resume_path = config.get("general", "resume_path", fallback=None)
if not resume_path:
    raise ValueError("Resume path is not set in config.ini.")

# ... other configuration ...
keywords = config.get("search", "keywords", fallback=None)
location = config.get("search", "location", fallback=None)
epoch_ago = int(config.get("search", "epoch_ago", fallback=Constants.DEFAULT_EPOCH_AGO))
limit = int(config.get("search", "limit", fallback=Constants.DEFAULT_JOB_LIMIT))
matching_method = config.get("matching", "method", fallback=Constants.DEFAULT_MATCHING_METHOD).lower()
threshold = int(config.get("matching", "threshold", fallback=Constants.DEFAULT_THRESHOLD))
user_description = config.get("matching", "description", fallback=None)
output_file_name = config.get("general", "output_path", fallback=None)

site_type = config.get("general", "site_type", fallback="linkedin")

# logging configuration
log_level = config.get("general", "log_level", fallback=Constants.DEFAULT_LOGGING_LEVEL)
log_file_path = config.get("general", "log_file", fallback=None)
if log_file_path:
    LOGGER.set_output_path(log_file_path)