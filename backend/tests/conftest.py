from __future__ import annotations

from unittest.mock import MagicMock
import pytest
import main


@pytest.fixture(autouse=True)
def mock_external_network_requests(monkeypatch):
    """
    Globally mock outgoing requests in tests to make the test suite deterministic,
    offline-capable, and fast without hitting real API quotas or external network delays.
    """
    def fake_requests_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()

        if "jsearch" in url:
            mock_resp.json.return_value = {
                "data": [
                    {
                        "employer_name": "TCS India",
                        "job_title": "Software Engineer",
                        "job_city": "Bengaluru",
                        "job_country": "India",
                        "job_apply_link": "https://www.linkedin.com/jobs/view/12345",
                        "job_employment_type": "Full-time",
                    },
                    {
                        "employer_name": "Infosys Limited",
                        "job_title": "Cloud DevOps Engineer",
                        "job_city": "Pune",
                        "job_country": "India",
                        "job_apply_link": "https://www.naukri.com/job-listings-12345",
                        "job_employment_type": "Full-time",
                    },
                ]
            }
        elif "adzuna" in url:
            mock_resp.json.return_value = {
                "results": [
                    {
                        "company": {"display_name": "Wipro Limited"},
                        "title": "Backend Developer",
                        "location": {"display_name": "Hyderabad, India"},
                        "redirect_url": "https://in.indeed.com/viewjob?jk=12345",
                        "contract_type": "Full-time",
                    }
                ]
            }
        else:
            mock_resp.json.return_value = {}

        return mock_resp

    monkeypatch.setattr(main.requests, "get", fake_requests_get)
