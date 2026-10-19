from __future__ import annotations

import os
import pytest
import matcher


def test_ml_role_model_loads_and_predicts():
    sample_devops = "Docker, Kubernetes, AWS, CI/CD pipeline automation, Terraform, and Linux administration."
    pred = matcher.predict_role_with_ml(sample_devops)
    assert pred in ("DevOps Engineer", "Full Stack Developer", "Machine Learning Engineer", "Data Analyst")


def test_ml_model_safe_handling_when_artifacts_missing(monkeypatch):
    # Monkeypatch to simulate missing model files
    monkeypatch.setattr(matcher, "_ml_role_model", None)
    monkeypatch.setattr(matcher, "_ml_role_vectorizer", None)
    monkeypatch.setattr(matcher, "_load_ml_model", lambda: (None, None))

    pred = matcher.predict_role_with_ml("Docker Kubernetes AWS")
    assert pred is None

    # predict_job_role should still succeed gracefully via fallback
    role = matcher.predict_job_role("Docker Kubernetes AWS")
    assert isinstance(role, str)
    assert len(role) > 0


def test_semantic_similarity_calculation():
    resume = "Python, FastAPI, Docker, and PostgreSQL developer."
    jd_match = "Seeking Python and FastAPI developer with Docker."
    jd_unrelated = "Looking for Head Chef with bakery and culinary expertise."

    score_match = matcher.calculate_similarity(resume, jd_match)
    score_unrelated = matcher.calculate_similarity(resume, jd_unrelated)

    assert 0 <= score_match <= 100
    assert 0 <= score_unrelated <= 100
    assert score_match > score_unrelated


def test_skill_gap_analysis():
    resume = "Experienced in Python and SQL."
    jd = "Required: Python, SQL, Docker, and AWS."

    gap = matcher.skill_gap_analysis(resume, jd)
    assert "matched_skills" in gap
    assert "missing_skills" in gap
    assert any("python" in s.lower() for s in gap["matched_skills"])
    assert any("docker" in s.lower() for s in gap["missing_skills"])


def test_learning_roadmap_generation():
    missing = ["Docker", "Kubernetes", "AWS"]
    roadmap = matcher.generate_learning_roadmap(missing)
    assert len(roadmap) == 3
    assert any("container" in step.lower() or "docker" in step.lower() for step in roadmap)
