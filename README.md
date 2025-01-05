# LinkedIn Scraper

This Python application automates the process of searching for jobs on LinkedIn. It uses Playwright for web automation and a modular design for extensibility.

## Features

* **Automated Job Search:** Searches for jobs on LinkedIn based on user-specified keywords, location, and filters.
* **Intelligent Job Matching:** Compares job descriptions to user-specified criteria using either fuzzy string matching or a Language Model (LLM).
* **Job Information Saving:** Saves relevant job information to a file for later review.
* **Robust Error Handling:** Includes comprehensive error handling and logging for enhanced reliability and debugging.
* **Modular Design:** Uses an abstract base class and modular design for maintainability and easy addition of new platforms.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Chrome Driver:** You can specify a path to your ChromeDriver using environment variables, or the `webdriver_manager` library will automatically manage this.
   If you choose to provide a ChromeDriver path, specify it in the `config.ini` file or as an environment variable.

3. **Configure `config.ini`:**
   Create a `config.ini` file in the root directory. This file contains:
   * ChromeDriver path
   * LinkedIn credentials (username, password)
   * Job search keywords, location, and filters
   * User's job description criteria
   * Matching method (fuzzy or LLM)
   * Logging configuration (log level, log file path)

**Note:** Never commit your `config.ini` file to version control; it contains sensitive information.

## Usage

1. **Run the Application:**
   ```bash
   python main.py
   ```

2. **Running Tests:**
   ```bash
   pytest
   ```

## Running the Application with Docker:

1. **Build the Docker Image:**
   ```bash
   docker build -t linkedin-scraper .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run --env-file .env linkedin-scraper
   ```

## Logging

The application uses a custom logging configuration defined in [src/logger.py](src/logger.py). Logs can be directed to a file by setting the `log_file_path` in the `config.ini` file.