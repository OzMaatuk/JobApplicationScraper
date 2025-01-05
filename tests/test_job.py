# tests/test_job.py
from src.models.job import Job

def test_job_model_str(test_job: Job):
    assert str(test_job) == "Job: Test Job at Test Company (Test Location)"