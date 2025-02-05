# src\logger.py

import logging
from src.constants.constants import Constants

logging.basicConfig(level=Constants.DEFAULT_LOGGING_LEVEL, format=Constants.LOGGING_FORMAT)


def get(name: str) -> logging.Logger:
    return logging.getLogger(name)

def set_output_path(path: str) -> None:
    file_handler = logging.FileHandler(path, encoding="utf-8")
    formatter = logging.Formatter(Constants.LOGGING_FORMAT)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

if Constants.LOG_TO_FILE:
    set_output_path(Constants.DEFAULT_LOGGING_FILE)
