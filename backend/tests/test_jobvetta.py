from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
import main


def test_jobvetta_disabled_when_placeholder_or_empty():
    with patch.object(main, "JOBVETTA_API_KEY", ""):
        assert main.fetch_jobvetta_jobs("Data Engineer") == []

    with patch.object(main, "JOBVETTA_API_KEY", "your_jobvetta_api_key"):
        assert main.fetch_jobvetta_jobs("Data Engineer") == []


def test_jobvetta_parses_valid_response():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {
        "jobs": [
            {
                "title": "Lead Data Engineer",
                "company_name": "Flipkart India",
                "location": "Bengaluru, Karnataka",
                "url": "https://careers.flipkart.com/jobs/123",
                "employment_type": "Full-time",
            },
            {
                "title": "Senior Data Engineer",
                "company_name": "Swiggy",
                "location": "Bengaluru, India",
                "url": "https://careers.swiggy.com/jobs/456",
                "employment_type": "Full-time",
            },
        ]
    }

    with patch.object(main, "JOBVETTA_API_KEY", "jv_live_sec_1234567890abcdef"), \
         patch("main.requests.get", return_value=mock_resp) as mock_get:
        jobs = main.fetch_jobvetta_jobs("Data Engineer", limit=4)
        assert len(jobs) == 2
        assert jobs[0]["job_title"] == "Lead Data Engineer"
        assert jobs[0]["company_name"] == "Flipkart India"
        assert jobs[0]["redirect_url"] == "https://careers.flipkart.com/jobs/123"
        assert jobs[0]["portal"] == "Jobvetta"

        # Verify exact request parameters sent to Jobvetta API
        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer jv_live_sec_1234567890abcdef"
        assert kwargs["params"]["q"] == "Data Engineer"
        assert kwargs["params"]["location"] == "Bengaluru"
        assert kwargs["params"]["days"] == "7"


def test_jobvetta_graceful_error_handling():
    mock_429 = MagicMock()
    mock_429.status_code = 429

    with patch.object(main, "JOBVETTA_API_KEY", "jv_live_sec_1234567890abcdef"), \
         patch("main.requests.get", return_value=mock_429):
        jobs = main.fetch_jobvetta_jobs("Data Engineer")
        assert jobs == []


def test_jobs_provider_status_reflects_jobvetta():
    with patch.object(main, "JOBVETTA_API_KEY", "jv_live_sec_1234567890abcdef"):
        status = main.jobs_provider_status()
        assert status["jobvetta_configured"] is True
        assert status["any_provider"] is True
        assert "Jobvetta" in status["provider_name"]
