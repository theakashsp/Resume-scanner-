from __future__ import annotations

import io
import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def _make_text_pdf(text: str) -> bytes:
    stream = f"BT\n/F1 12 Tf\n72 712 Td\n({text}) Tj\nET\n"
    stream_bytes = stream.encode("latin1")
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    obj4 = b"4 0 obj\n<< /Length " + str(len(stream_bytes)).encode("ascii") + b" >>\nstream\n" + stream_bytes + b"endstream\nendobj\n"
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    header = b"%PDF-1.4\n"
    offsets = [0]
    curr = len(header)
    for obj in (obj1, obj2, obj3, obj4, obj5):
        offsets.append(curr)
        curr += len(obj)

    xref = f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("ascii")
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("ascii")

    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{curr}\n%%EOF\n".encode("ascii")
    return header + obj1 + obj2 + obj3 + obj4 + obj5 + xref + trailer


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Resume Analyzer"
    assert "health" in data


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "parser_status" in data
    assert "ml_model_status" in data
    assert "jobs_provider" in data
    assert "ai_provider" in data


def test_platform_stats_and_features(client: TestClient):
    res_stats = client.get("/api/platform-stats")
    assert res_stats.status_code == 200
    assert "domains_supported" in res_stats.json()

    res_feat = client.get("/api/features")
    assert res_feat.status_code == 200
    assert len(res_feat.json()["features"]) > 0


def test_fetch_jobs_endpoint(client: TestClient):
    response = client.post(
        "/api/fetch-jobs",
        json={"recommended_roles": ["Software Developer", "Full Stack Developer"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "jobs_by_role" in data
    assert "jobs_count" in data


def test_analyze_empty_file_rejected(client: TestClient):
    response = client.post(
        "/analyze",
        files={"file": ("resume.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400
    assert "empty" in response.text.lower()


def test_analyze_non_pdf_rejected(client: TestClient):
    response = client.post(
        "/analyze",
        files={"file": ("resume.docx", b"PK\x03\x04...", "application/vnd.openxmlformats")},
    )
    assert response.status_code == 400
    assert "only pdf" in response.text.lower()


def test_analyze_scanned_pdf_returns_clear_message(client: TestClient):
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    blank_bytes = buf.getvalue()

    response = client.post(
        "/analyze",
        files={"file": ("scanned_resume.pdf", blank_bytes, "application/pdf")},
    )
    assert response.status_code == 422
    data = response.json()
    assert data.get("code") == "SCANNED_PDF"
    assert "scanned or image-only" in data.get("error", "").lower()


def test_analyze_valid_resume_success_with_fallback(client: TestClient):
    resume_text = (
        "Alice Smith\n"
        "Email: alice.smith@example.com | Phone: 9876543212 | Pune, India\n\n"
        "PROFESSIONAL SUMMARY\n"
        "DevOps and Cloud Engineer with 3 years of hands-on infrastructure experience.\n\n"
        "TECHNICAL SKILLS\n"
        "Docker, Kubernetes, AWS, Terraform, CI/CD, Python, Linux, Git\n\n"
        "PROFESSIONAL EXPERIENCE\n"
        "Cloud Engineer | Wipro Technologies (2022 - Present)\n"
        "- Deployed microservices on Kubernetes cluster reducing deployment failure rate by 40%.\n"
        "- Managed AWS infrastructure with Terraform automating multi-region setup.\n"
        "- Led containerization of 15 internal services using Docker.\n\n"
        "EDUCATION\n"
        "B.E. in Information Technology | Pune University | CGPA: 8.7 / 10\n\n"
        "PROJECTS & CERTIFICATIONS\n"
        "AWS Certified Solutions Architect Associate\n"
    )
    pdf_bytes = _make_text_pdf(resume_text)

    response = client.post(
        "/analyze",
        files={"file": ("alice_resume.pdf", pdf_bytes, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()

    # Core response fields
    assert "ats_score" in data
    assert 0 <= data["ats_score"] <= 100
    assert "target_role" in data
    assert "recommended_roles" in data
    assert len(data["recommended_roles"]) > 0
    assert "current_skills" in data
    assert "Docker" in data["current_skills"] or "Kubernetes" in data["current_skills"]
    assert "learning_roadmap" in data
    assert len(data["learning_roadmap"]) > 0
    assert "scoring_breakdown" in data
    assert "evidence_explanations" in data
    assert "disclaimer" in data
    assert "jobs_by_role" in data


def test_analyze_with_optional_job_description(client: TestClient):
    resume_text = (
        "Bob Kumar\n"
        "Email: bob.kumar@example.com | Phone: 9876543213 | Hyderabad, India\n\n"
        "SUMMARY\n"
        "Python backend engineer with FastAPI and PostgreSQL expertise.\n\n"
        "SKILLS\n"
        "Python, FastAPI, PostgreSQL, Git, Docker\n\n"
        "EXPERIENCE\n"
        "Backend Developer | TCS (2022 - Present)\n"
        "- Designed REST APIs with FastAPI processing 500k queries daily.\n\n"
        "EDUCATION\n"
        "B.Tech in Computer Science | JNTU Hyderabad\n"
    )
    pdf_bytes = _make_text_pdf(resume_text)
    target_jd = "Required: Python, FastAPI, Docker, and AWS experience for Senior Backend role."

    response = client.post(
        "/analyze",
        files={"file": ("bob_resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_description": target_jd},
    )
    assert response.status_code == 200
    data = response.json()
    assert "scoring_breakdown" in data
    assert data["scoring_breakdown"].get("job_compatibility_score") is not None
    assert "job_specific_analysis" in data
    assert data["job_specific_analysis"] is not None


def test_readiness_endpoint(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["parser_ready"] is True
    assert data["local_nlp_engine"] == "ready"
    assert "optional_integrations" in data


def test_analyze_invalid_content_type(client: TestClient):
    sample_text = "John Doe - Software Developer"
    pdf_bytes = _make_text_pdf(sample_text)
    response = client.post(
        "/analyze",
        files={"file": ("resume.pdf", pdf_bytes, "text/plain")},
    )
    assert response.status_code == 400
    assert "invalid file content-type" in response.text.lower()


def test_analyze_oversized_job_description(client: TestClient):
    sample_text = "John Doe - Software Developer"
    pdf_bytes = _make_text_pdf(sample_text)
    oversized_jd = "Python " * 5000  # > 25,000 characters
    response = client.post(
        "/analyze",
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_description": oversized_jd},
    )
    assert response.status_code == 400
    assert "exceeds maximum allowed length" in response.text.lower()


def test_analyze_path_traversal_filename_handled_safely(client: TestClient):
    resume_text = (
        "Jane Traversal\n"
        "Email: jane@example.com | Phone: 9876543210\n"
        "Software Engineer with Python, React, and SQL experience.\n"
    )
    pdf_bytes = _make_text_pdf(resume_text)
    response = client.post(
        "/analyze",
        files={"file": ("../../../../etc/passwd.pdf", pdf_bytes, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ats_score"] >= 0


def test_gemini_failure_graceful_fallback_to_heuristic(client: TestClient, monkeypatch):
    import main

    class BrokenClient:
        class models:
            @staticmethod
            def generate_content(*args, **kwargs):
                raise RuntimeError("Simulated Gemini API 503 Service Unavailable / Rate Limit")

    monkeypatch.setattr(main, "_genai_client", BrokenClient())

    resume_text = (
        "Alice Fallback\n"
        "Email: alice@example.com | Phone: 9876543219 | Bengaluru\n\n"
        "SUMMARY\n"
        "Full Stack Developer with 3 years Python and React experience.\n\n"
        "SKILLS\n"
        "Python, React, PostgreSQL, Docker\n\n"
        "EXPERIENCE\n"
        "Software Engineer | Infosys (2022 - Present)\n"
        "- Built microservices using Python and Docker.\n"
    )
    pdf_bytes = _make_text_pdf(resume_text)

    response = client.post(
        "/analyze",
        files={"file": ("fallback_resume.pdf", pdf_bytes, "application/pdf")},
    )
    # Must NOT fail with 502 Bad Gateway; must fall back gracefully to heuristic engine
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_source"] == "heuristic"
    assert "Python" in data["current_skills"]
    assert 0 <= data["ats_score"] <= 100


def test_auth_me_unauthenticated_and_authenticated(client: TestClient):
    # 1. Unauthenticated request without token returns 401
    res_no_token = client.get("/api/auth/me")
    assert res_no_token.status_code == 401

    # 2. Invalid token returns 401
    res_bad_token = client.get("/api/auth/me", headers={"Authorization": "Bearer fake_token_xyz"})
    assert res_bad_token.status_code == 401

    # 3. Register and Login to obtain token
    client.post(
        "/api/auth/register",
        json={"name": "Auth Me User", "email": "authme@example.com", "password": "SecurePassword123!"},
    )
    login_res = client.post(
        "/api/auth/login",
        json={"email": "authme@example.com", "password": "SecurePassword123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # 4. Valid token accesses /api/auth/me successfully
    res_authed = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_authed.status_code == 200
    assert res_authed.json()["user"]["email"] == "authme@example.com"

    # 5. Logout revokes token
    logout_res = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200

    # 6. Subsequent request with revoked token returns 401
    res_after_logout = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_after_logout.status_code == 401

