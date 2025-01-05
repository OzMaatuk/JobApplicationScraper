# tests/test_description_matcher.py

import pytest
from src.utils.description_matcher import DescriptionMatcher
from llm_utils import LLMUtils

def test_description_matcher_fuzz():
    matcher = DescriptionMatcher()
    assert matcher.matches("Software Engineer", "Software Engineer") is True

def test_description_matcher_llm(mocker):
    # Mock LLMManager instance inside the DescriptionMatcher instance.
    mock_llm = mocker.Mock(spec=LLMUtils)
    mocker.patch.object(LLMUtils, "generate_text", return_value="90")

    matcher = DescriptionMatcher(method="llm")

    assert matcher.matches("Software Engineer", "Senior Software Engineer") is True
    LLMUtils.generate_text.assert_called_once_with("Given the job description: Software Engineer, and the user description: Senior Software Engineer, rate the similarity between the two descriptions from 0 to 100. return only the final score.")

def test_description_matcher_invalid_method():
    with pytest.raises(ValueError, match="Invalid matching method"):
        DescriptionMatcher(method="invalid").matches("","")

def test_fuzz_matches_different_thresholds():
    """Test fuzzy matching with different thresholds."""
    matcher = DescriptionMatcher(method="fuzz", threshold=51)
    string1 = "Software Engineer"
    string2 = "Software Developer"
    assert matcher._fuzz_matches(string1, string2) is True
    
    matcher = DescriptionMatcher(method="fuzz", threshold=90)
    assert matcher._fuzz_matches(string1, string2) is False