# src\logger.py

import logging
from src.constants import DEFAULT_LOGGING_LEVEL, LOGGING_FORMAT, LOG_TO_FILE, DEFAULT_LOGGING_FILE

logging.basicConfig(level=DEFAULT_LOGGING_LEVEL, format=LOGGING_FORMAT)


def get(name: str) -> logging.Logger:
    return logging.getLogger(name)

def set_output_path(path: str) -> None:
    file_handler = logging.FileHandler(path, encoding="utf-8")
    formatter = logging.Formatter(LOGGING_FORMAT)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

if LOG_TO_FILE:
    set_output_path(DEFAULT_LOGGING_FILE)
