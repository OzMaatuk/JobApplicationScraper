# src/constants.py

# --- LinkedIn URLs ---
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"
LINKEDIN_JOBS_SEARCH_URL = "https://www.linkedin.com/jobs/search/?"

# --- Locators ---
class Locators:
    class Login:
        USERNAME_FIELD = "input#username"
        PASSWORD_FIELD = "input#password"
        LOGIN_BUTTON = "button[data-litms-control-urn='login-submit']"

    class Search:
        SEARCH_RESULTS = "//li[contains(@class, 'occludable-update')]"
        JOBS_SEARCH_KEYWORDS = "input[name='keywords']"
        JOBS_SEARCH_LOCATION = "input[name='location']"
        NUM_OF_SEARCH_RESULTS = "//*[@id=\"main\"]/div/div[2]/div[1]/header/div[1]/small"

    class Job:
        TITLE = "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/div/h1"
        COMPANY = "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a"
        LOCATION = "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span[1]"
        URL = "//a[@class='ember-view']"
        DESCRIPTION = "//div[@id='job-details']"
        EASY_APPLY = "//button[span[text()='Easy Apply']]"
        APPLY = "//button[span[text()='Apply']]"
        SEARCH_RESULTS = "//li[contains(@class, 'occludable-update')]"

# --- Configuration ---
# CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.ini")  # Adjust relative path as needed

# --- Other Constants ---
DEFAULT_TIMEOUT = 10
DEFAULT_FUZZ_THRESHOLD = 80
DEFAULT_MATCHING_METHOD = "fuzz"

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

NUM_OF_JOBS_IN_PAGE = 25
URL_PAGE_NUM_PARAMETER = "&start="