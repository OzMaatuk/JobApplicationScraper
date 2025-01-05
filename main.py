# main.py

from dataclasses import asdict
import json
from driver import initialize_driver
import src.logger as LOGGER
import datetime
from typing import List
from dotenv import load_dotenv

from src.linkedin.facade import LinkedInFacade
from src.linkedin.exceptions import LinkedInAutomationError
from src.models.job import Job

logger = LOGGER.get(__name__)
load_dotenv()

def _save_results(path: str, jobs: List[Job]):
    """Saves application results to a JSON file."""
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        output_file_name = f"{path}_{current_date}.json"

        with open(output_file_name, 'w', encoding='utf-8') as f:
            json.dump(list(map(asdict, jobs)), f, ensure_ascii=False, indent=4)
        logger.info(f"Results saved to {output_file_name}")
    except Exception as e:
        logger.error(f"Error saving results to JSON: {e}")

def main():
    try:
        logger.info("Load Configuration")
        from config import matching_method, threshold, linkedin_password, linkedin_username, keywords, location, time_ago, user_description, output_file_name, log_level, chrome_user_data_path
        if log_level: logger.setLevel(level=log_level)

        logger.info("Initialize Playwright")
        browser = initialize_driver(False, chrome_user_data_path)
        page = browser.pages[0]

        logger.info("Initialize and run the facade")
        facade = LinkedInFacade(page, matching_method, threshold)
        
        logger.info("Log in to LinkedIn")
        facade.login(linkedin_username, linkedin_password)
        
        # Search for Jobs
        jobs = facade.search_jobs(keywords, location, time_ago, limit=6)
        jobs_to_apply = facade.filter_jobs(jobs, user_description)

        logger.info("Close the browser")
        browser.close()

        logger.info("Save results")
        _save_results(output_file_name, jobs_to_apply)

    except Exception as e:
        error_msg = f"Failed in main execution: {str(e)}"
        logger.error(error_msg)
        raise LinkedInAutomationError(error_msg) from e

if __name__ == "__main__":
    main()