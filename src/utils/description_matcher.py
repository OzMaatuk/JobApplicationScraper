# src/utils/description_matcher.py

import src.logger as LOGGER
# from fuzzywuzzy import fuzz
from llm_utils import LLMUtils

from src.constants.constants import Constants


logger = LOGGER.get(__name__)

class DescriptionMatcher:
    """Matches job descriptions using various methods."""

    def __init__(self, method: str = Constants.DEFAULT_MATCHING_METHOD, threshold: int = Constants.DEFAULT_THRESHOLD, api_key: str = None):
        logger.debug("DescriptionMatcher instance created")
        self.method = method
        self.threshold = threshold
        self.llm = LLMUtils(api_key)

    def matches(self, job_description: str, user_description: str) -> bool:
        logger.debug("DescriptionMatcher.matches")
        # logger.debug(f"Method: {self.method}")
        # logger.debug(f"Threshold: {self.threshold}")
        # logger.debug(f"Job Description: {job_description}")
        # logger.debug(f"User Description: {user_description}")
        
        if self.method == "llm":
            prompt = f"Given the current job description: {job_description}, and the desired job description: {user_description}, rate from 0 to 100 if the current job description is matching the desired job description. return only the final score."
            logger.debug(f"LLM prompt: {prompt}")
            score = int(self.llm.generate_text(prompt))
            logger.debug(f"Generated score: {score}")
            logger.debug(f"Check if score >= self.threshold: {score} >= {self.threshold}")
            return score >= self.threshold
        elif self.method == "fuzz":
            raise NotImplementedError("Fuzzy matching implementation was removed.")
            # return self._fuzz_matches(job_description, user_description)
        else:
            logger.error(f"Invalid matching method in config file: {self.method}")
            raise ValueError(f"Invalid matching method in config file: {self.method}")  

    def _fuzz_matches(self, job_description: str, user_description: str) -> bool:
        logger.debug("DescriptionMatcher._fuzz_matches")
        similarity_ratio = 0 # fuzz.ratio(job_description, user_description)
        logger.debug(f"Check if similarity_ratio >= self.threshold: {similarity_ratio} >= {self.threshold}")
        return similarity_ratio >= self.threshold