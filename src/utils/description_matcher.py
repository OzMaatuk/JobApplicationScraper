# src/utils/description_matcher.py

import src.logger as LOGGER
from fuzzywuzzy import fuzz
from llm_utils import LLMUtils

from src.constants import DEFAULT_FUZZ_THRESHOLD, DEFAULT_MATCHING_METHOD


logger = LOGGER.get(__name__)

class DescriptionMatcher:
    """Matches job descriptions using various methods."""

    def __init__(self, method: str = DEFAULT_MATCHING_METHOD, threshold: int = DEFAULT_FUZZ_THRESHOLD, api_key: str = None):
        logger.debug("DescriptionMatcher instance created")
        self.method = method
        self.threshold = threshold
        self.llm = LLMUtils()

    def matches(self, job_description: str, user_description: str) -> bool:
        logger.debug("DescriptionMatcher.matches")
        if self.method == "llm":
            prompt = f"Given the job description: {job_description}, and the user description: {user_description}, rate the similarity between the two descriptions from 0 to 100. return only the final score."
            score = int(self.llm.generate_text(prompt))
            logger.debug(f"Check if score >= self.threshold: {score} >= {self.threshold}")
            return score >= self.threshold
        elif self.method == "fuzz":
            return self._fuzz_matches(job_description, user_description)
        else:
            raise ValueError(f"Invalid matching method in config file: {self.method}")  

    def _fuzz_matches(self, job_description: str, user_description: str) -> bool:
        logger.debug("DescriptionMatcher._fuzz_matches")
        similarity_ratio = fuzz.ratio(job_description, user_description) * 10
        logger.debug(f"Check if similarity_ratio >= self.threshold: {similarity_ratio} >= {self.threshold}")
        return similarity_ratio >= self.threshold