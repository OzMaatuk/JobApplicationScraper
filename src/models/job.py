# src/models/job.py

from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass  # Use dataclass for concise class definition
class Job:
    title: str
    company: str
    location: str
    url: str
    easy_apply: bool
    description: Optional[str] = None #Some job postings don´t include the description initially.
    epoch_ago: Optional[str] = None
    # Add other relevant attributes as needed (e.g., seniority level, job type, etc.)
    application_status: Optional[str] = None # "Applied", "Not Applied", "Failed" etc.
    raw_data: Optional[Dict] = None # Store the unprocessed or original data format


    def __str__(self): # Customize string representation
        return f"Job: {self.title} at {self.company} ({self.location})"