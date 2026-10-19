from __future__ import annotations

import pytest
from skills import (
    compute_missing_skills,
    detect_domain,
    evaluate_ats_score,
    extract_comprehensive_skills,
    extract_professional_skills,
    infer_roles_from_skills,
    sanitize_skills,
)


def test_negation_filtering_prevents_false_positives():
    text_with_negation = (
        "Software developer with strong Python, FastAPI, and PostgreSQL skills. "
        "Have no practical experience in Kubernetes or Docker. "
        "Also unfamiliar with Flutter."
    )
    skills_data = extract_comprehensive_skills(text_with_negation)
    extracted = skills_data["all_skills"]

    assert "Python" in extracted
    assert "FastAPI" in extracted
    assert "PostgreSQL" in extracted
    # Negated skills must NOT be present
    assert "Kubernetes" not in extracted
    assert "Docker" not in extracted


def test_symbol_and_short_skills_extraction():
    text = "Proficient in C, C++, C#, R, Go, and .NET core with Git and Linux shell."
    skills_data = extract_comprehensive_skills(text)
    extracted = skills_data["all_skills"]

    assert "C" in extracted
    assert "C++" in extracted
    assert "C#" in extracted
    assert ".NET" in extracted
    assert "Git / GitHub" in extracted
    assert "Linux / Shell" in extracted


def test_multi_domain_skill_extraction():
    # Commerce
    commerce_text = "Accounts Executive with expertise in Tally Prime, GST filing, Bank Reconciliation, and Financial Modeling."
    com_skills = extract_comprehensive_skills(commerce_text, domain="Commerce & Finance")
    assert "Tally ERP / Prime" in com_skills["all_skills"]
    assert "GST Compliance" in com_skills["all_skills"]
    assert "Bank Reconciliation" in com_skills["all_skills"]

    # Core Engineering
    eng_text = "Mechanical design engineer with hands-on proficiency in AutoCAD 2D/3D, SolidWorks, MATLAB, and Six Sigma quality control."
    eng_skills = extract_comprehensive_skills(eng_text, domain="Core Engineering")
    assert "AutoCAD 2D/3D" in eng_skills["all_skills"]
    assert "SolidWorks / CATIA" in eng_skills["all_skills"]
    assert "MATLAB & Simulink" in eng_skills["all_skills"]

    # Healthcare
    health_text = "Clinical coordinator experienced in Patient Care, Clinical Documentation, Electronic Health Records (EHR), and Infection Control."
    health_skills = extract_comprehensive_skills(health_text, domain="Healthcare")
    assert "Patient Care & Triage" in health_skills["all_skills"]
    assert "Clinical Documentation" in health_skills["all_skills"]
    assert "Electronic Health Records (EHR)" in health_skills["all_skills"]


def test_explainable_ats_score_breakdown():
    resume_text = (
        "John Doe\n"
        "Email: john.doe@example.com | Phone: 9876543210 | Bengaluru, India\n\n"
        "PROFESSIONAL SUMMARY\n"
        "Full Stack Developer with 3 years of experience architecting scalable REST APIs and responsive web apps.\n\n"
        "SKILLS\n"
        "Python, React, TypeScript, Node.js, PostgreSQL, Docker, AWS, Git\n\n"
        "EXPERIENCE\n"
        "Software Engineer | Infosys (2022 - Present)\n"
        "- Architected high-concurrency microservices reducing latency by 35% across 2 million daily requests.\n"
        "- Led migration of legacy monolith to containerized Docker services on AWS.\n"
        "- Deployed CI/CD pipelines with GitHub Actions improving release frequency by 50%.\n\n"
        "EDUCATION\n"
        "B.Tech in Computer Science | VTU Bengaluru (2018 - 2022) | CGPA: 8.9 / 10\n\n"
        "PROJECTS\n"
        "E-Commerce Platform: Built full-stack platform using React and FastAPI supporting 10,000 active users.\n"
    )

    eval_result = evaluate_ats_score(resume_text, domain="Information Technology")

    assert 0 <= eval_result["overall_ats_score"] <= 100
    assert 0 <= eval_result["general_quality_score"] <= 100
    assert 0 <= eval_result["skill_coverage_score"] <= 100
    assert 0 <= eval_result["practical_evidence_score"] <= 100
    assert len(eval_result["evidence_explanations"]) > 0
    assert "weights" in eval_result or "scoring_weights" in eval_result
    assert "disclaimer" in eval_result
    # Good resume with contact, summary, experience, education, metrics, action verbs should score well
    assert eval_result["overall_ats_score"] >= 65


def test_ats_score_with_job_description_compatibility():
    resume_text = "Experienced Python, FastAPI, and Docker backend engineer with PostgreSQL database skills."
    job_desc = "Looking for a Backend Python Engineer with FastAPI, Docker, and PostgreSQL experience."

    eval_result = evaluate_ats_score(
        resume_text,
        domain="Information Technology",
        job_description=job_desc,
    )

    assert eval_result["job_compatibility_score"] is not None
    assert eval_result["job_compatibility_score"] >= 70
    assert eval_result["job_specific_analysis"] is not None
    assert "Python" in eval_result["job_specific_analysis"]["matched_requirements"] or len(eval_result["job_specific_analysis"]["matched_requirements"]) > 0


def test_non_it_candidates_not_unfairly_penalized():
    commerce_resume = (
        "Jane Smith\n"
        "Email: jane.smith@example.com | Phone: 9876543211 | Mumbai, India\n\n"
        "SUMMARY\n"
        "Senior Accounts Executive with 4 years experience in taxation, audit, and commercial accounts.\n\n"
        "EXPERIENCE\n"
        "Accounts Lead | Reliance Industries (2021 - Present)\n"
        "- Managed monthly GST returns and statutory tax filings saving 15% in reconciliation time.\n"
        "- Supervised annual auditing and bank reconciliation across 5 corporate accounts.\n\n"
        "SKILLS\n"
        "Tally Prime, GST Compliance, Advanced MS Excel, Taxation & TDS, Financial Reporting, Auditing Standards\n\n"
        "EDUCATION\n"
        "B.Com (Bachelor of Commerce) | Mumbai University | CGPA: 8.5 / 10\n"
    )

    eval_result = evaluate_ats_score(commerce_resume, domain="Commerce & Finance")
    assert eval_result["overall_ats_score"] >= 60
    assert eval_result["skill_coverage_score"] >= 60


def test_job_specific_3tier_categorization():
    resume_text = (
        "Frontend Engineer with proficiency in React, JavaScript, and PostgreSQL. "
        "Built responsive dashboards and optimized web performance."
    )
    job_desc = (
        "Frontend Specialist opening. "
        "Required: React, JavaScript. "
        "Preferred: Next.js. Nice to have: Docker. "
        "3+ years experience required."
    )

    result = evaluate_ats_score(resume_text, domain="Information Technology", job_description=job_desc)
    assert result["job_compatibility_score"] is not None
    jd_analysis = result["job_specific_analysis"]
    assert jd_analysis is not None

    # Explicitly demonstrated (directly in resume)
    assert "React.js" in jd_analysis["explicitly_demonstrated"] or "JavaScript" in jd_analysis["explicitly_demonstrated"]
    # Potentially demonstrated (Next.js is related to React in web track)
    assert any("next" in s.lower() for s in jd_analysis["potentially_demonstrated"])
    # Not found (Docker is not mentioned and not in web group)
    assert any("docker" in s.lower() for s in jd_analysis["not_found"])
    # Caveat note
    assert "not proof" in jd_analysis["evidence_note"].lower()


def test_enhanced_negation_phrases():
    text = (
        "Skilled Python and FastAPI developer. "
        "Not experienced in Docker or Kubernetes. "
        "Have not used Rust. "
        "Lacks knowledge of Swift."
    )
    extracted = extract_comprehensive_skills(text)["all_skills"]
    assert "Python" in extracted
    assert "FastAPI" in extracted
    assert "Docker" not in extracted
    assert "Kubernetes" not in extracted
    assert "Rust" not in extracted
    assert "Swift" not in extracted


def test_multi_domain_synthetic_dataset():
    domains_and_resumes = [
        (
            "Cloud & DevOps",
            "DevOps Engineer. Skills: AWS, Docker, Kubernetes, Terraform, CI/CD pipelines, Linux shell scripting. 3 years experience.",
        ),
        (
            "Network Engineering",
            "Network Administrator. Skills: Cisco Networking, TCP/IP, Wireshark, Routing (BGP/OSPF), Network Firewalls, DNS / DHCP.",
        ),
        (
            "Healthcare",
            "Clinical Coordinator. Skills: Patient Care & Triage, Clinical Documentation, Electronic Health Records (EHR), Infection Control.",
        ),
        (
            "Education",
            "Academic Faculty. Skills: Curriculum Planning, Classroom Management, Pedagogical Delivery, Student Assessment, EdTech Tools (LMS).",
        ),
        (
            "Management",
            "Project Lead. Skills: Project Management, Stakeholder Management, Strategic Planning, Agile/Scrum, Process Optimization.",
        ),
    ]

    for expected_domain, text in domains_and_resumes:
        detected = detect_domain(text)
        assert detected == expected_domain, f"Expected {expected_domain}, detected {detected}"
        ats_eval = evaluate_ats_score(text, domain=detected)
        assert ats_eval["overall_ats_score"] >= 50, f"ATS score for {expected_domain} was {ats_eval['overall_ats_score']}"
        assert ats_eval["skill_coverage_score"] >= 50, f"Skill coverage for {expected_domain} was {ats_eval['skill_coverage_score']}"

