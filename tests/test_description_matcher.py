# tests/test_description_matcher.py

import pytest
from src.utils.description_matcher import DescriptionMatcher
from llm_utils import LLMUtils

@pytest.mark.skip(reason="Fuzzy matching implementation was removed.")
def test_description_matcher_fuzz():
    matcher = DescriptionMatcher()
    assert matcher.matches("Software Engineer", "Software Engineer") is True

def test_description_matcher_llm(mocker):
    mocker.patch.object(LLMUtils, "generate_text", return_value="90")
    matcher = DescriptionMatcher(method="llm")
    assert matcher.matches("Software Engineer", "Senior Software Engineer") is True
    LLMUtils.generate_text.assert_called_once_with("Given the current job description: Software Engineer, and the desired job description: Senior Software Engineer, rate from 0 to 100 if the current job description is matching the desired job description. return only the final score.")

def test_description_matcher_invalid_method():
    with pytest.raises(ValueError, match="Invalid matching method"):
        DescriptionMatcher(method="invalid").matches("","")

@pytest.mark.skip(reason="Fuzzy matching implementation was removed.")
def test_fuzz_matches_different_thresholds():
    """Test fuzzy matching with different thresholds."""
    matcher = DescriptionMatcher(method="fuzz", threshold=51)
    string1 = "Software Engineer"
    string2 = "Software Developer"
    assert matcher._fuzz_matches(string1, string2) is True
    
    matcher = DescriptionMatcher(method="fuzz", threshold=90)
    assert matcher._fuzz_matches(string1, string2) is False