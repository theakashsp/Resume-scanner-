from __future__ import annotations

import re
from pdfminer.high_level import extract_text
from docx import Document

from skills import (
    extract_comprehensive_skills,
    extract_education_details,
    extract_experience_details,
    extract_projects_and_activities,
    detect_domain,
)


def normalize_utf8(text: str) -> str:
    """
    Normalize any parser output into UTF-8-safe text on Windows consoles.
    Replaces unsupported/surrogate chars instead of crashing.
    """
    if not text:
        return ""
    return str(text).encode("utf-8", errors="replace").decode("utf-8", errors="replace")


def extract_resume_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return normalize_utf8(extract_text(file_path))
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return normalize_utf8("\n".join([para.text for para in doc.paragraphs]))
    else:
        return ""


def parse_resume(file_path: str) -> dict:
    """
    Comprehensive resume parser returning cleaned text, categorized skills,
    experience details, education & CGPA/GPA, and projects/activities.
    """
    raw_text = extract_resume_text(file_path)
    cleaned_text = normalize_utf8(raw_text)

    skills_data = extract_comprehensive_skills(cleaned_text)
    education_data = extract_education_details(cleaned_text)
    experience_data = extract_experience_details(cleaned_text)
    projects_data = extract_projects_and_activities(cleaned_text)
    domain = detect_domain(cleaned_text)

    return {
        "cleaned_text": cleaned_text,
        "domain": domain,
        "skills": skills_data["all_skills"],
        "skills_categorized": skills_data,
        "experience": experience_data,
        "experience_years": experience_data["total_years"],
        "education": education_data,
        "education_degrees": education_data["all_degrees"],
        "cgpa": education_data["cgpa_or_gpa"],
        "projects_and_activities": projects_data,
    }
