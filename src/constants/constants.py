# src/constants/constants.py

class Constants():

    # --- Configuration ---
    # CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.ini")  # Adjust relative path as needed

    # --- Other Constants ---
    DEFAULT_TIMEOUT = 10
    DEFAULT_THRESHOLD = 80
    DEFAULT_MATCHING_METHOD = "llm"
    DEFAULT_JOB_LIMIT = 10
    DEFAULT_EPOCH_AGO = 86400

    # --- Logging ---
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'  # Standard logging format
    DEFAULT_LOGGING_LEVEL = "DEBUG"
    DEFAULT_LOGGING_FILE = "data/logs/main.log"
    DEFAULT_TEST_LOGGING_FILE = "data/logs/test.log"
    LOG_TO_FILE = False

    # --- Google Generative AI ---
    GOOGLE_API_MODEL = "gemini-1.5-flash" # Default model for Google Generative AI

    # --- Application Status Constants (for tracking applications) ---
    APPLICATION_STATUS_APPLIED = "Applied"
    APPLICATION_STATUS_NOT_APPLIED = "Not Applied"
    APPLICATION_STATUS_FAILED = "Failed"
    
    # --- URLs ---
    LOGIN_URL = None
    FEED_URL = None
    JOBS_SEARCH_URL = None

    # --- Locators ---
    class Locators:
        def __init__(self):
            raise NotImplementedError("Abstarct Constants class does not have Locators implementation.")

    NUM_OF_JOBS_IN_PAGE = 25
    URL_PAGE_NUM_PARAMETER = None

    # --- Easy Apply Form Constants ---
    class EasyApplyForm:
        def __init__(self):
            raise NotImplementedError("Abstarct Constants class does not have EasyApplyForm implementation.")
