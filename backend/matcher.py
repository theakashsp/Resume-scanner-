from __future__ import annotations

# ==============================================================================
# TECH STACK: [Matcher & Multi-Dimensional Profile Evaluator]
# Evaluates Skills, Experience, Education & CGPA, Projects & Other Activities,
# with semantic / TF-IDF similarity, weighted skill matching, and role mapping.
# ==============================================================================
import os
import re
from typing import Any

# Optional high-efficiency SentenceTransformer loader
_transformer_model = None
try:
    from sentence_transformers import SentenceTransformer, util
    _transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    _transformer_model = None

from skills import (
    extract_comprehensive_skills,
    extract_education_details,
    extract_experience_details,
    extract_projects_and_activities,
    generate_multi_skill_career_tracks,
    calculate_score_breakdown,
    detect_domain,
)

COMMON_SKILLS = [
    "c", "c++", "c#", "java", "python", "javascript", "typescript",
    "react", "node", "express", "sql", "mongodb", "postgresql", "redis",
    "aws", "docker", "kubernetes", "git", "linux", "html", "css",
    "data structures", "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "spring boot", "django", "fastapi"
]

SKILL_WEIGHTS = {
    # Core Languages
    "c": 1.4,
    "c++": 1.5,
    "c#": 1.4,
    "java": 1.5,
    "python": 1.5,
    "javascript": 1.4,
    "typescript": 1.4,
    "sql": 1.3,
    # Frameworks & Platforms
    "spring boot": 1.5,
    "react": 1.4,
    "node": 1.3,
    "django": 1.3,
    "fastapi": 1.3,
    # Cloud & DevOps
    "aws": 1.4,
    "docker": 1.3,
    "kubernetes": 1.4,
    "ci/cd": 1.2,
    "linux": 1.2,
    # AI & Data
    "machine learning": 1.8,
    "deep learning": 1.8,
    "data analysis": 1.4,
    "data structures": 1.6,
    "mongodb": 1.2,
    "postgresql": 1.2,
}


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """
    Calculate semantic similarity score (0-100) between resume and job description.
    Uses SentenceTransformer if available, or token-level Jaccard/TF-IDF similarity.
    """
    if _transformer_model is not None:
        try:
            embeddings = _transformer_model.encode([resume_text, job_description])
            similarity = util.cos_sim(embeddings[0], embeddings[1])
            return round(float(similarity[0][0]) * 100, 2)
        except Exception:
            pass

    # High-accuracy token fallback
    tokens_r = set(re.findall(r"\b[a-zA-Z0-9+#]{2,}\b", resume_text.lower()))
    tokens_j = set(re.findall(r"\b[a-zA-Z0-9+#]{2,}\b", job_description.lower()))
    if not tokens_j:
        return 50.0
    intersection = tokens_r & tokens_j
    union = tokens_r | tokens_j
    jaccard = len(intersection) / len(union) if union else 0.0
    scaled = min(98.0, 30.0 + jaccard * 120.0)
    return round(scaled, 2)


def skill_gap_analysis(resume_text: str, job_description: str) -> dict[str, Any]:
    """
    Perform deep skill gap analysis identifying matched skills, missing skills,
    and individual skill match scores.
    """
    resume_skills_data = extract_comprehensive_skills(resume_text)
    jd_skills_data = extract_comprehensive_skills(job_description)

    resume_all = {s.lower(): s for s in resume_skills_data["all_skills"]}
    jd_all = {s.lower(): s for s in jd_skills_data["all_skills"]}

    matched_keys = set(resume_all.keys()) & set(jd_all.keys())
    missing_keys = set(jd_all.keys()) - set(resume_all.keys())

    matched_skills = [jd_all[k] for k in matched_keys]
    missing_skills = [jd_all[k] for k in missing_keys]

    skill_scores: dict[str, float] = {}
    for k, skill_name in jd_all.items():
        if k in matched_keys:
            skill_scores[skill_name] = 100.0
        else:
            if _transformer_model is not None:
                try:
                    s_emb = _transformer_model.encode(skill_name)
                    r_emb = _transformer_model.encode(resume_text[:2000])
                    sim = util.cos_sim(s_emb, r_emb)
                    skill_scores[skill_name] = round(float(sim[0][0]) * 100, 2)
                    continue
                except Exception:
                    pass
            skill_scores[skill_name] = 20.0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_scores": skill_scores,
    }


def weighted_skill_match(resume_skills: list[str], job_description: str) -> tuple[float, list[str]]:
    """
    Calculate weighted skill match score against a job description.
    """
    jd_lower = job_description.lower()
    resume_lower = {s.lower() for s in resume_skills}

    total_weight = 0.0
    matched_weight = 0.0
    matched_skills = []

    for skill, weight in SKILL_WEIGHTS.items():
        if skill in jd_lower:
            total_weight += weight
            if skill in resume_lower or any(skill in r for r in resume_lower):
                matched_weight += weight
                matched_skills.append(skill.title())

    if total_weight == 0.0:
        return 75.0, resume_skills[:4]

    score = (matched_weight / total_weight) * 100
    return round(score, 2), matched_skills


def generate_learning_roadmap(missing_skills: list[str]) -> list[str]:
    """
    Generate actionable step-by-step career milestone roadmap for missing skills.
    """
    roadmap: list[str] = []
    for skill in missing_skills:
        sl = skill.lower()
        if "c++" in sl or "c " in sl:
            roadmap.append("Master modern C++ (C++17/20), STL containers, smart pointers, and multithreading.")
        elif "python" in sl:
            roadmap.append("Complete advanced Python: OOP, asynchronous programming, and REST API development (FastAPI/Django).")
        elif "java" in sl or "spring" in sl:
            roadmap.append("Build a production-grade Spring Boot microservices backend with JPA & PostgreSQL.")
        elif "react" in sl:
            roadmap.append("Develop a full-stack responsive web application with React 19, state management, and API integration.")
        elif "aws" in sl or "cloud" in sl:
            roadmap.append("Earn the AWS Certified Cloud Practitioner / Solutions Architect Associate certification.")
        elif "docker" in sl or "kubernetes" in sl:
            roadmap.append("Containerize multi-container web apps with Docker and deploy them on a Kubernetes cluster.")
        elif "sql" in sl:
            roadmap.append("Practice complex SQL queries: window functions, index optimization, and relational database schema design.")
        elif "machine learning" in sl or "ai" in sl:
            roadmap.append("Implement end-to-end ML models: data preprocessing with Pandas, model training with Scikit-Learn/PyTorch, and FastAPI deployment.")
        elif "data structures" in sl:
            roadmap.append("Solve 50+ core DSA problems (Trees, Graphs, Dynamic Programming) on LeetCode/HackerRank.")
        else:
            roadmap.append(f"Deepen practical hands-on experience and build a portfolio project demonstrating {skill}.")
    return roadmap


def evaluate_full_candidate_profile(resume_text: str) -> dict[str, Any]:
    """
    Comprehensive multi-dimensional evaluator analyzing:
    1. Skills (all programming languages like C, C++, Java, Python, Web, Cloud, Databases)
    2. Experience (years, seniority tier, internships)
    3. Education & CGPA/GPA/CPA (degree, grades, academic standing)
    4. Projects & Extracurricular Activities (projects, certifications, hackathons, open source)
    5. Multi-Skill Career Tracks across all strong skill sets
    6. 4-Pillar Score Breakdown & Overall ATS Score
    """
    skills_data = extract_comprehensive_skills(resume_text)
    edu_data = extract_education_details(resume_text)
    exp_data = extract_experience_details(resume_text)
    proj_data = extract_projects_and_activities(resume_text)
    domain = detect_domain(resume_text)

    # Calculate skill score
    total_skills_count = len(skills_data["all_skills"])
    skill_score = min(98, max(35, 45 + total_skills_count * 4))

    score_breakdown = calculate_score_breakdown(
        skills_score=int(skill_score),
        experience_score=exp_data["experience_score"],
        education_score=edu_data["education_score"],
        projects_activities_score=proj_data["projects_activities_score"],
    )

    career_tracks = generate_multi_skill_career_tracks(
        matched_skills=skills_data["all_skills"],
        experience_info=exp_data,
        domain=domain,
    )

    return {
        "domain": domain,
        "skills_data": skills_data,
        "education_data": edu_data,
        "experience_data": exp_data,
        "projects_data": proj_data,
        "career_tracks": career_tracks["career_tracks"],
        "recommended_roles": career_tracks["recommended_roles"],
        "score_breakdown": score_breakdown,
        "overall_ats_score": score_breakdown["overall_ats_score"],
    }


def predict_job_role(resume_text: str) -> str:
    """
    Predict primary recommended job role.
    """
    eval_result = evaluate_full_candidate_profile(resume_text)
    roles = eval_result["recommended_roles"]
    return roles[0] if roles else "Software Developer"
