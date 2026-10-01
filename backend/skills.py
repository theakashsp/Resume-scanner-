from __future__ import annotations

# ==============================================================================
# TECH STACK: [Domain Taxonomy & Multi-Dimensional NLP Engine]
# Comprehensive Extraction: Skills, Experience, Education & CGPA/GPA,
# Projects & Other Activities, Multi-Skill Career Tracks & 4-Pillar Scoring
# ==============================================================================
import re
from typing import Any

DOMAIN_PROFILES: dict[str, dict[str, Any]] = {
    "Cloud & DevOps": {
        "signals": (
            "aws", "azure", "gcp", "cloud", "devops", "kubernetes", "docker",
            "terraform", "ci/cd", "ec2", "s3", "lambda", "cloudformation", "ansible",
        ),
        "roles": [
            "Cloud Engineer", "DevOps Engineer", "AWS Solutions Architect",
            "Site Reliability Engineer", "Platform Engineer", "Cloud Support Engineer",
        ],
        "skill_pool": [
            "aws", "azure", "gcp", "ec2", "s3", "lambda", "cloudformation",
            "docker", "kubernetes", "terraform", "ansible", "jenkins", "ci/cd",
            "linux", "monitoring", "vpc", "iam", "rds", "eks", "helm",
        ],
    },
    "Information Technology": {
        "signals": (
            "python", "java", "javascript", "react", "sql", "api", "software",
            "developer", "programming", "machine learning", "data", "cloud", "devops",
            "c++", "c", "c#", "node", "backend", "frontend",
        ),
        "roles": [
            "Software Developer", "Full Stack Developer", "Backend Developer",
            "Frontend Developer", "Data Analyst", "C/C++ Systems Engineer",
            "Java Developer", "Python Developer",
        ],
        "skill_pool": [
            "c", "c++", "c#", "java", "python", "javascript", "typescript", "react",
            "node.js", "sql", "git", "docker", "aws", "rest api", "agile", "testing",
            "html", "css", "microservices", "mongodb", "postgresql", "redis",
            "fastapi", "django", "spring boot", "data structures", "algorithms",
        ],
    },
    "Embedded & Systems Engineering": {
        "signals": (
            "c", "c++", "embedded", "microcontroller", "arduino", "raspberry pi",
            "rtos", "firmware", "device driver", "iot", "arm", "system programming",
        ),
        "roles": [
            "Embedded Systems Engineer", "C/C++ Systems Developer", "Firmware Engineer",
            "IoT Solutions Engineer", "System Software Engineer",
        ],
        "skill_pool": [
            "c", "c++", "embedded c", "microcontrollers", "arm", "rtos", "firmware",
            "linux kernel", "device drivers", "i2c", "spi", "uart", "iot", "assembly",
            "system programming", "socket programming", "multithreading",
        ],
    },
    "Data Science & AI": {
        "signals": (
            "machine learning", "deep learning", "nlp", "computer vision", "data science",
            "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "data analysis",
        ),
        "roles": [
            "Data Scientist", "AI/ML Engineer", "Data Analyst",
            "Machine Learning Researcher", "Data Engineer",
        ],
        "skill_pool": [
            "python", "r", "machine learning", "deep learning", "nlp", "computer vision",
            "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "sql",
            "power bi", "tableau", "statistics", "data visualization",
        ],
    },
    "Network Engineering": {
        "signals": (
            "cisco", "routing", "switching", "tcp/ip", "wireshark", "bgp", "ospf",
            "firewall", "vlan", "dns", "dhcp", "lan", "wan", "network", "ccna", "juniper",
        ),
        "roles": [
            "Network Engineer", "NOC Engineer", "Network Administrator",
            "Security Network Engineer", "Infrastructure Engineer",
        ],
        "skill_pool": [
            "cisco", "routing", "switching", "tcp/ip", "wireshark", "bgp", "ospf",
            "firewall", "vlan", "dns", "dhcp", "lan", "wan", "network security", "ccna",
        ],
    },
    "Commerce & Finance": {
        "signals": (
            "accounting", "finance", "commerce", "gst", "tally", "excel", "audit",
            "banking", "tax", "bookkeeping", "economics", "financial analysis",
        ),
        "roles": [
            "Accounts Executive", "Financial Analyst", "Tax Associate",
            "Business Development Executive", "Operations Coordinator",
        ],
        "skill_pool": [
            "financial analysis", "ms excel", "tally", "gst compliance",
            "financial reporting", "bank reconciliation", "budgeting", "forecasting",
        ],
    },
    "Marketing & Operations": {
        "signals": (
            "marketing", "digital marketing", "seo", "sem", "branding", "operations",
            "supply chain", "logistics", "customer relations", "crm", "sales",
        ),
        "roles": [
            "Marketing Executive", "Digital Marketing Specialist", "Operations Executive",
            "Business Analyst", "Customer Relations Manager",
        ],
        "skill_pool": [
            "digital marketing", "seo", "content strategy", "operations management",
            "customer relations", "crm", "market research", "campaign management",
        ],
    },
    "Healthcare": {
        "signals": (
            "nursing", "patient care", "clinical", "pharmacy", "medical", "hospital",
            "healthcare", "diagnosis", "b.pharm", "b.sc nursing",
        ),
        "roles": [
            "Staff Nurse", "Pharmacy Assistant", "Medical Records Coordinator",
            "Healthcare Administrator", "Clinical Research Coordinator",
        ],
        "skill_pool": [
            "patient care", "clinical documentation", "medical terminology",
            "healthcare compliance", "pharmacology basics", "vital signs monitoring",
        ],
    },
    "Education": {
        "signals": (
            "teaching", "education", "curriculum", "classroom", "tutoring", "pedagogy",
            "b.ed", "lecturer", "academic", "training",
        ),
        "roles": [
            "Academic Coordinator", "Corporate Trainer", "Teaching Assistant",
            "Instructional Designer", "Education Counselor",
        ],
        "skill_pool": [
            "curriculum planning", "classroom management", "lesson delivery",
            "student assessment", "educational technology", "communication",
        ],
    },
    "Management": {
        "signals": (
            "management", "leadership", "mba", "project management", "team lead",
            "strategy", "stakeholder", "business management", "hr",
        ),
        "roles": [
            "Management Trainee", "Project Coordinator", "HR Executive",
            "Business Operations Manager", "Assistant Manager",
        ],
        "skill_pool": [
            "project management", "leadership", "stakeholder management",
            "business communication", "team management", "strategic planning",
        ],
    },
    "Arts & Humanities": {
        "signals": (
            "english", "literature", "history", "psychology", "sociology",
            "content", "writing", "journalism", "media", "communication",
        ),
        "roles": [
            "Content Writer", "Social Media Executive", "HR Coordinator",
            "Customer Support Specialist", "Research Assistant",
        ],
        "skill_pool": [
            "written communication", "research", "content writing", "editing",
            "critical thinking", "presentation", "customer service",
        ],
    },
    "Administration": {
        "signals": (
            "administration", "office", "clerical", "reception", "coordination",
            "scheduling", "documentation", "executive assistant",
        ),
        "roles": [
            "Administrative Assistant", "Office Coordinator", "Executive Assistant",
            "Operations Assistant", "Front Office Executive",
        ],
        "skill_pool": [
            "ms office", "scheduling", "documentation", "coordination",
            "email etiquette", "record keeping", "customer handling",
        ],
    },
    "Core Engineering": {
        "signals": (
            "mechanical", "civil", "electrical", "electronics", "manufacturing",
            "autocad", "solidworks", "thermodynamics", "circuit", "matlab",
        ),
        "roles": [
            "Graduate Engineer Trainee", "Design Engineer", "Site Engineer",
            "Quality Engineer", "Production Engineer",
        ],
        "skill_pool": [
            "autocad", "technical drawing", "safety standards", "quality control",
            "project documentation", "team coordination", "matlab", "solidworks",
        ],
    },
    "General / Fresher": {
        "signals": ("fresher", "graduate", "intern", "trainee", "entry level", "bachelor"),
        "roles": [
            "Graduate Trainee", "Management Trainee", "Junior Executive",
            "Customer Support Associate", "Operations Trainee",
        ],
        "skill_pool": [
            "communication", "ms office", "teamwork", "time management",
            "problem solving", "adaptability", "customer relations",
        ],
    },
}

_STOPWORDS = frozenset({
    "and", "the", "for", "with", "from", "your", "have", "this", "that", "email",
    "phone", "mobile", "address", "name", "resume", "curriculum", "vitae", "gmail",
    "yahoo", "hotmail", "contact", "objective", "summary", "profile", "skills",
    "experience", "education", "project", "projects", "india", "linkedin",
    "bengaluru", "bangalore", "mumbai", "delhi", "chennai", "hyderabad", "pune",
    "kolkata", "karnataka", "maharashtra", "engineering",
})

_NON_RESUME_SIGNALS = (
    "chapter ", "textbook", "assignment", "question paper", "table of contents",
    "bibliography", "isbn", "abstract", "syllabus", "lecture notes", "unit ",
    "lesson plan", "research paper", "journal article", "theorem", "exercise ",
    "study note", "random image", "image log", "text snippet", "figure ",
    "diagram ", "equation ", "solve the following", "marks)", "total marks",
)

_RESUME_SIGNALS = (
    "resume", "curriculum vitae", "cv", "experience", "education", "skills",
    "internship", "projects", "objective", "summary", "work history", "employment",
    "certification", "qualification", "profile", "responsibilities", "achievements",
    "extracurricular", "academic", "cgpa", "gpa", "b.tech", "bachelor",
)

# ==============================================================================
# EXACT BOUNDARY PROGRAMMING LANGUAGES & CORE TECH TAXONOMY
# Explicitly handles single-letter and symbol-based skills: C, C++, C#, R, etc.
# ==============================================================================
LANGUAGE_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("c", re.compile(r"(?<![a-zA-Z0-9_])c(?![a-zA-Z0-9_+#])", re.IGNORECASE), "C"),
    ("c++", re.compile(r"(?<![a-zA-Z0-9_])(?:c\+\+|cpp)(?![a-zA-Z0-9_])", re.IGNORECASE), "C++"),
    ("c#", re.compile(r"(?<![a-zA-Z0-9_])(?:c#|csharp)(?![a-zA-Z0-9_])", re.IGNORECASE), "C#"),
    ("python", re.compile(r"\bpython(?:3)?\b", re.IGNORECASE), "Python"),
    ("java", re.compile(r"\bjava\b(?!\s*script)", re.IGNORECASE), "Java"),
    ("javascript", re.compile(r"\b(?:javascript|js)\b", re.IGNORECASE), "JavaScript"),
    ("typescript", re.compile(r"\b(?:typescript|ts)\b", re.IGNORECASE), "TypeScript"),
    ("r", re.compile(r"(?<![a-zA-Z0-9_])r(?:\s+programming|\s+language)?(?![a-zA-Z0-9_])", re.IGNORECASE), "R"),
    ("sql", re.compile(r"\b(?:sql|mysql|postgresql|postgres|plsql|sqlite|mssql|t-sql)\b", re.IGNORECASE), "SQL"),
    ("go", re.compile(r"\b(?:golang|go\s+language)\b|(?<![a-zA-Z0-9_])go(?![a-zA-Z0-9_])", re.IGNORECASE), "Go"),
    ("rust", re.compile(r"\brust\b", re.IGNORECASE), "Rust"),
    ("php", re.compile(r"\bphp\b", re.IGNORECASE), "PHP"),
    ("ruby", re.compile(r"\bruby\b", re.IGNORECASE), "Ruby"),
    ("kotlin", re.compile(r"\bkotlin\b", re.IGNORECASE), "Kotlin"),
    ("swift", re.compile(r"\bswift\b", re.IGNORECASE), "Swift"),
    ("scala", re.compile(r"\bscala\b", re.IGNORECASE), "Scala"),
    ("dart", re.compile(r"\bdart\b", re.IGNORECASE), "Dart"),
    ("html/css", re.compile(r"\b(?:html5?|css3?|html/css|html\s*&\s*css)\b", re.IGNORECASE), "HTML/CSS"),
    ("matlab", re.compile(r"\bmatlab\b", re.IGNORECASE), "MATLAB"),
    ("assembly", re.compile(r"\b(?:assembly|x86|arm\s+assembly)\b", re.IGNORECASE), "Assembly"),
]

FRAMEWORK_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("react", re.compile(r"\b(?:react|react\.js|reactjs)\b", re.IGNORECASE), "React.js"),
    ("node", re.compile(r"\b(?:node|node\.js|nodejs)\b", re.IGNORECASE), "Node.js"),
    ("express", re.compile(r"\b(?:express|express\.js|expressjs)\b", re.IGNORECASE), "Express.js"),
    ("angular", re.compile(r"\bangular(?:\.js)?\b", re.IGNORECASE), "Angular"),
    ("vue", re.compile(r"\bvue(?:\.js)?\b", re.IGNORECASE), "Vue.js"),
    ("spring boot", re.compile(r"\bspring\s*boot\b", re.IGNORECASE), "Spring Boot"),
    ("django", re.compile(r"\bdjango\b", re.IGNORECASE), "Django"),
    ("fastapi", re.compile(r"\bfastapi\b", re.IGNORECASE), "FastAPI"),
    ("flask", re.compile(r"\bflask\b", re.IGNORECASE), "Flask"),
    ("nextjs", re.compile(r"\bnext(?:\.js|js)?\b", re.IGNORECASE), "Next.js"),
    (".net", re.compile(r"\b(?:\.net|dotnet|asp\.net)\b", re.IGNORECASE), ".NET"),
    ("tensorflow", re.compile(r"\btensorflow\b", re.IGNORECASE), "TensorFlow"),
    ("pytorch", re.compile(r"\bpytorch\b", re.IGNORECASE), "PyTorch"),
    ("pandas", re.compile(r"\bpandas\b", re.IGNORECASE), "Pandas"),
    ("numpy", re.compile(r"\bnumpy\b", re.IGNORECASE), "NumPy"),
    ("scikit-learn", re.compile(r"\b(?:scikit-learn|sklearn)\b", re.IGNORECASE), "Scikit-Learn"),
]

CLOUD_DEVOPS_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("aws", re.compile(r"\b(?:aws|amazon\s+web\s+services)\b", re.IGNORECASE), "AWS"),
    ("azure", re.compile(r"\b(?:azure|microsoft\s+azure)\b", re.IGNORECASE), "Azure"),
    ("gcp", re.compile(r"\b(?:gcp|google\s+cloud)\b", re.IGNORECASE), "Google Cloud (GCP)"),
    ("docker", re.compile(r"\bdocker\b", re.IGNORECASE), "Docker"),
    ("kubernetes", re.compile(r"\b(?:kubernetes|k8s)\b", re.IGNORECASE), "Kubernetes"),
    ("terraform", re.compile(r"\bterraform\b", re.IGNORECASE), "Terraform"),
    ("ci/cd", re.compile(r"\b(?:ci/cd|jenkins|gitlab\s*ci|github\s*actions)\b", re.IGNORECASE), "CI/CD"),
    ("linux", re.compile(r"\b(?:linux|ubuntu|centos|bash|shell\s+scripting)\b", re.IGNORECASE), "Linux / Shell"),
    ("ansible", re.compile(r"\bansible\b", re.IGNORECASE), "Ansible"),
]

DATABASE_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("mongodb", re.compile(r"\bmongodb\b", re.IGNORECASE), "MongoDB"),
    ("postgresql", re.compile(r"\b(?:postgresql|postgres)\b", re.IGNORECASE), "PostgreSQL"),
    ("mysql", re.compile(r"\bmysql\b", re.IGNORECASE), "MySQL"),
    ("redis", re.compile(r"\bredis\b", re.IGNORECASE), "Redis"),
    ("oracle", re.compile(r"\boracle\s+db\b|\boracle\s+database\b", re.IGNORECASE), "Oracle DB"),
    ("nosql", re.compile(r"\bnosql\b", re.IGNORECASE), "NoSQL"),
]

TOOL_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("git", re.compile(r"\b(?:git|github|gitlab)\b", re.IGNORECASE), "Git / GitHub"),
    ("rest api", re.compile(r"\b(?:rest\s*api|restful\s*api|apis?)\b", re.IGNORECASE), "REST APIs"),
    ("microservices", re.compile(r"\bmicroservices\b", re.IGNORECASE), "Microservices"),
    ("data structures", re.compile(r"\b(?:data\s+structures|dsa|algorithms)\b", re.IGNORECASE), "Data Structures & Algorithms"),
    ("postman", re.compile(r"\bpostman\b", re.IGNORECASE), "Postman"),
    ("power bi", re.compile(r"\bpower\s*bi\b", re.IGNORECASE), "Power BI"),
    ("tableau", re.compile(r"\btableau\b", re.IGNORECASE), "Tableau"),
    ("jira", re.compile(r"\bjira\b", re.IGNORECASE), "Jira / Agile"),
    ("figma", re.compile(r"\bfigma\b", re.IGNORECASE), "Figma"),
]

SOFT_SKILL_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("problem solving", re.compile(r"\bproblem\s+solving\b", re.IGNORECASE), "Problem Solving"),
    ("teamwork", re.compile(r"\b(?:teamwork|collaboration|team\s+player)\b", re.IGNORECASE), "Team Collaboration"),
    ("communication", re.compile(r"\b(?:communication\s+skills|verbal\s+communication|written\s+communication)\b", re.IGNORECASE), "Communication"),
    ("leadership", re.compile(r"\b(?:leadership|lead|mentored)\b", re.IGNORECASE), "Leadership"),
    ("time management", re.compile(r"\btime\s+management\b", re.IGNORECASE), "Time Management"),
    ("analytical thinking", re.compile(r"\b(?:analytical|critical\s+thinking)\b", re.IGNORECASE), "Analytical Thinking"),
]


# ==============================================================================
# COMPREHENSIVE MULTI-DIMENSIONAL EXTRACTION FUNCTIONS
# ==============================================================================

def extract_comprehensive_skills(text: str) -> dict[str, Any]:
    """
    Extract all skills cleanly without omitting short or symbol-based skills (C, C++, C#, Java, Python, etc.)
    """
    languages: list[str] = []
    frameworks: list[str] = []
    cloud_devops: list[str] = []
    databases: list[str] = []
    tools: list[str] = []
    soft_skills: list[str] = []
    all_matched: list[str] = []
    seen_lower: set[str] = set()

    def add_skill(cat_list: list[str], canonical: str):
        low = canonical.lower()
        if low not in seen_lower:
            seen_lower.add(low)
            cat_list.append(canonical)
            all_matched.append(canonical)

    for _, pat, name in LANGUAGE_PATTERNS:
        if pat.search(text):
            add_skill(languages, name)

    for _, pat, name in FRAMEWORK_PATTERNS:
        if pat.search(text):
            add_skill(frameworks, name)

    for _, pat, name in CLOUD_DEVOPS_PATTERNS:
        if pat.search(text):
            add_skill(cloud_devops, name)

    for _, pat, name in DATABASE_PATTERNS:
        if pat.search(text):
            add_skill(databases, name)

    for _, pat, name in TOOL_PATTERNS:
        if pat.search(text):
            add_skill(tools, name)

    for _, pat, name in SOFT_SKILL_PATTERNS:
        if pat.search(text):
            add_skill(soft_skills, name)

    return {
        "languages": languages,
        "frameworks": frameworks,
        "cloud_devops": cloud_devops,
        "databases": databases,
        "tools": tools,
        "soft_skills": soft_skills,
        "all_skills": all_matched,
    }


def extract_education_details(text: str) -> dict[str, Any]:
    """
    Extract Degree, College/University, CGPA / GPA / CPA / Percentage and Academic Rating.
    """
    lower = text.lower()

    # Degree patterns
    degrees_found: list[str] = []
    degree_map = [
        (r"\bb\.?\s*tech(?:nology)?\b", "B.Tech (Bachelor of Technology)"),
        (r"\bb\.?\s*e\.?\b", "B.E. (Bachelor of Engineering)"),
        (r"\bm\.?\s*tech(?:nology)?\b", "M.Tech (Master of Technology)"),
        (r"\bmca\b", "MCA (Master of Computer Applications)"),
        (r"\bbca\b", "BCA (Bachelor of Computer Applications)"),
        (r"\bb\.?\s*sc\b", "B.Sc (Bachelor of Science)"),
        (r"\bm\.?\s*sc\b", "M.Sc (Master of Science)"),
        (r"\bmba\b", "MBA (Master of Business Administration)"),
        (r"\bb\.?\s*com\b", "B.Com (Bachelor of Commerce)"),
        (r"\bbba\b", "BBA (Bachelor of Business Administration)"),
        (r"\bph\.?d\b|\bdoctorate\b", "Ph.D / Doctorate"),
        (r"\bdiploma\b", "Diploma"),
        (r"\bbachelor(?:'s)?\b", "Bachelor's Degree"),
        (r"\bmaster(?:'s)?\b", "Master's Degree"),
    ]

    for pat, label in degree_map:
        if re.search(pat, lower):
            degrees_found.append(label)

    primary_degree = degrees_found[0] if degrees_found else "Bachelor's Degree"

    # CGPA / GPA / CPA / Percentage extraction
    cgpa_val: str | None = None
    cgpa_num: float | None = None

    # Specific patterns for CGPA / GPA / CPA / Percentage
    gpa_patterns = [
        # e.g., "CGPA: 8.8 / 10", "CGPA 9.1", "GPA: 3.8/4.0", "CPA: 3.9"
        r"\b(?:cgpa|gpa|cpa|sgpa)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:/\s*(10|4|100))?",
        # e.g., "8.8 / 10 CGPA" or "8.8/10"
        r"\b([0-9]\.[0-9]{1,2})\s*/\s*(10|4)(?:\.0)?\b",
        # e.g., "85% or 85.5 %"
        r"\b([6-9][0-9](?:\.[0-9]{1,2})?)\s*%",
        # e.g., "Percentage: 84.5"
        r"\b(?:percentage|percent|marks?|aggregate)\s*[:=-]?\s*([0-9]{2}(?:\.[0-9]+)?)\s*%?",
    ]

    for pat in gpa_patterns:
        m = re.search(pat, lower)
        if m:
            raw_num = m.group(1)
            scale = m.group(2) if len(m.groups()) >= 2 and m.group(2) else None
            try:
                val = float(raw_num)
                if scale == "4" or val <= 4.0 and not "%" in m.group(0):
                    cgpa_val = f"{val:.2f} / 4.0 GPA"
                    cgpa_num = (val / 4.0) * 10.0
                elif scale == "100" or val > 10.0:
                    cgpa_val = f"{val:.1f}%"
                    cgpa_num = val / 10.0
                else:
                    cgpa_val = f"{val:.2f} / 10.0 CGPA"
                    cgpa_num = val
                break
            except ValueError:
                pass

    # Graduation year / status
    grad_year_match = re.search(r"\b(201[5-9]|202[0-9]|2030)\b", text)
    grad_year = grad_year_match.group(0) if grad_year_match else "Recent Graduate"
    is_pursuing = bool(re.search(r"\b(pursuing|final year|current|ongoing|expected)\b", lower))

    # Calculate Education Score (0-100)
    edu_score = 65
    if degrees_found:
        edu_score += 10
    if cgpa_num is not None:
        if cgpa_num >= 8.5:
            edu_score += 20
        elif cgpa_num >= 7.5:
            edu_score += 15
        elif cgpa_num >= 6.0:
            edu_score += 10
    else:
        edu_score += 10  # default reasonable base

    if any(k in lower for k in ("distinction", "first class", "honors", "dean's list", "rank")):
        edu_score = min(100, edu_score + 5)

    edu_score = max(40, min(98, edu_score))

    academic_standing = "Excellent" if edu_score >= 85 else "Very Good" if edu_score >= 70 else "Good"

    return {
        "primary_degree": primary_degree,
        "all_degrees": degrees_found,
        "cgpa_or_gpa": cgpa_val or "Not explicitly listed",
        "cgpa_numeric": cgpa_num,
        "graduation_year": grad_year,
        "is_pursuing": is_pursuing,
        "academic_standing": academic_standing,
        "education_score": edu_score,
        "summary": f"{primary_degree} • {cgpa_val or 'Standard Academic Standing'} ({grad_year})",
    }


def extract_experience_details(text: str) -> dict[str, Any]:
    """
    Extract total experience years, internship details, seniority level, and experience score.
    """
    lower = text.lower()

    # Years extraction
    years_found: list[float] = []
    for match in re.finditer(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of\s+experience)?", lower):
        try:
            val = float(match.group(1))
            if 0.5 <= val <= 35:
                years_found.append(val)
        except ValueError:
            pass

    # Timeline date ranges e.g. 2021 - 2024 or Jan 2022 - Present
    date_ranges = re.findall(
        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.?\s*(201[0-9]|202[0-9])\s*[-–—to]{1,3}\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.?\s*(201[0-9]|202[0-9])|present|current)\b",
        lower,
    )
    if date_ranges and not years_found:
        years_found.append(min(len(date_ranges) * 1.0, 6.0))

    total_years = max(years_found) if years_found else 0.0

    has_internship = bool(re.search(r"\b(intern|internship|trainee|apprentice)\b", lower))
    has_fulltime = bool(re.search(r"\b(full-time|full time|software engineer|developer|consultant|analyst)\b", lower))
    has_fresher = bool(re.search(r"\b(fresher|entry level|graduate|final year student|student)\b", lower))

    if total_years >= 5:
        tier = "Senior Level (5+ years)"
        base_score = 90
    elif total_years >= 3:
        tier = "Mid-Level (3-5 years)"
        base_score = 82
    elif total_years >= 1:
        tier = "Junior Level (1-2 years)"
        base_score = 74
    elif has_internship:
        tier = "Entry Level with Internship Experience"
        base_score = 68
    elif has_fresher:
        tier = "Fresher / College Graduate"
        base_score = 58
    else:
        tier = "Entry Level / Graduate"
        base_score = 60

    # Boost score if candidate has leadership / impact action verbs
    action_verbs = sum(
        1 for v in ("led", "designed", "architected", "deployed", "scaled", "optimized", "managed", "built")
        if v in lower
    )
    exp_score = min(98, base_score + min(action_verbs * 2, 10))

    return {
        "total_years": total_years,
        "display_years": f"{total_years:g}+ years" if total_years > 0 else ("Internship Experience" if has_internship else "Fresher / Entry-Level"),
        "tier": tier,
        "has_internship": has_internship,
        "experience_score": int(exp_score),
        "summary": f"{tier} ({f'{total_years:g} yrs' if total_years > 0 else 'Fresh graduate'})",
    }


def extract_projects_and_activities(text: str) -> dict[str, Any]:
    """
    Extract Academic / Personal Projects, Professional Certifications,
    and Extracurricular / Other Activities (Hackathons, Open Source, Leadership, Competitions).
    """
    lower = text.lower()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    projects: list[str] = []
    certifications: list[str] = []
    activities: list[str] = []

    # Detect projects from text
    in_project_section = False
    in_cert_section = False
    in_activity_section = False

    for line in lines:
        ll = line.lower()
        # Section triggers
        if any(h in ll for h in ("projects", "academic projects", "key projects", "personal projects")):
            in_project_section = True
            in_cert_section = False
            in_activity_section = False
            continue
        elif any(h in ll for h in ("certifications", "certificates", "courses", "licenses")):
            in_project_section = False
            in_cert_section = True
            in_activity_section = False
            continue
        elif any(h in ll for h in ("extracurricular", "achievements", "activities", "hackathons", "competitions", "volunteering", "positions of responsibility")):
            in_project_section = False
            in_cert_section = False
            in_activity_section = True
            continue
        elif any(h in ll for h in ("education", "skills", "experience", "work history", "contact")):
            in_project_section = False
            in_cert_section = False
            in_activity_section = False
            continue

        if in_project_section and len(line) > 5 and len(line) < 140:
            if not any(k in ll for k in ("technologies used", "github", "demo", "overview")):
                projects.append(line)
        elif in_cert_section and len(line) > 4 and len(line) < 120:
            certifications.append(line)
        elif in_activity_section and len(line) > 5 and len(line) < 140:
            activities.append(line)

    # Keyword detections for certifications
    cert_keywords = [
        ("aws certified", "AWS Certified Cloud Practitioner / Solutions Architect"),
        ("azure certified", "Microsoft Certified: Azure Fundamentals / Developer"),
        ("google cloud certified", "Google Cloud Certified Associate"),
        ("hackerrank", "HackerRank Problem Solving / Coding Badge"),
        ("leetcode", "LeetCode Algorithmic Problem Solving"),
        ("coursera", "Coursera Professional Specialization"),
        ("udemy", "Udemy Technical Course Completion"),
        ("ccna", "Cisco CCNA Certification"),
        ("oracle certified", "Oracle Certified Java Associate / Professional"),
    ]
    for kw, label in cert_keywords:
        if kw in lower and label not in certifications:
            certifications.append(label)

    # Keyword detections for Extracurriculars & Other Activities
    activity_keywords = [
        ("hackathon", "Hackathon Participant & Solution Builder"),
        ("smart india hackathon", "Smart India Hackathon (SIH) Participant"),
        ("open source", "Open Source Contributor (GitHub)"),
        ("coding competition", "Competitive Programming & Coding Contests"),
        ("codechef", "CodeChef Competitive Programming"),
        ("codeforces", "Codeforces Contestant"),
        ("club", "College Technical / Cultural Club Member"),
        ("lead", "Team Lead / Event Coordinator"),
        ("volunteer", "Community & Social Volunteering"),
        ("paper presentation", "Technical Paper Presentation / IEEE Conference"),
        ("workshop", "Technical Workshop Organizing / Participation"),
    ]
    for kw, label in activity_keywords:
        if kw in lower and label not in activities:
            activities.append(label)

    # Score calculation for projects & activities (0-100)
    score = 55
    if projects:
        score += min(len(projects) * 8, 20)
    else:
        score += 10
    if certifications:
        score += min(len(certifications) * 7, 15)
    if activities:
        score += min(len(activities) * 5, 12)

    proj_score = max(45, min(96, score))

    return {
        "projects": projects[:5],
        "certifications": certifications[:5],
        "extracurricular_activities": activities[:5],
        "projects_activities_score": int(proj_score),
    }


# ==============================================================================
# MULTI-SKILL CAREER TRACKS & ROLE RECOMMENDATIONS
# Guarantees that if a person has C, C++, Java, Python, React, etc.,
# they receive targeted career tracks for EVERY key skill set!
# ==============================================================================

def generate_multi_skill_career_tracks(
    matched_skills: list[str],
    experience_info: dict[str, Any],
    domain: str,
) -> dict[str, Any]:
    """
    Generate multi-skill career tracks across C, C++, Java, Python, Web, Cloud, Data, etc.
    """
    skills_lower = {s.lower() for s in matched_skills}
    tracks: list[dict[str, Any]] = []
    all_recommended_roles: list[str] = []

    # 1. C & C++ Systems / Embedded Track
    has_c = any(s in skills_lower for s in ("c", "c++", "c/c++", "assembly", "embedded c"))
    if has_c:
        matched_in_track = [s for s in matched_skills if s.lower() in ("c", "c++", "c/c++", "embedded c", "data structures", "linux / shell", "git / github")]
        roles = [
            "C/C++ Systems Software Engineer",
            "Embedded Systems Engineer",
            "Firmware Developer",
            "High-Performance Computing Engineer",
        ]
        score = min(96, 75 + len(matched_in_track) * 6)
        tracks.append({
            "track_name": "C & C++ Systems & Embedded Engineering",
            "badge": "Systems & Embedded",
            "icon": "cpu",
            "match_score": int(score),
            "key_skills": matched_in_track or ["C", "C++"],
            "recommended_roles": roles,
            "description": "Low-level systems programming, embedded firmware, high-performance computing, and OS-level architecture.",
        })
        all_recommended_roles.extend(roles[:2])

    # 2. Python & AI / Data Track
    has_python = any(s in skills_lower for s in ("python", "django", "fastapi", "flask", "pandas", "numpy", "tensorflow", "pytorch", "machine learning"))
    if has_python:
        matched_in_track = [s for s in matched_skills if s.lower() in ("python", "django", "fastapi", "flask", "pandas", "numpy", "tensorflow", "pytorch", "machine learning", "sql", "git / github")]
        roles = [
            "Python Backend Developer",
            "AI/ML Engineer",
            "Data Engineer",
            "Automation Software Engineer",
        ]
        score = min(96, 76 + len(matched_in_track) * 5)
        tracks.append({
            "track_name": "Python, AI & Data Engineering",
            "badge": "Python & AI",
            "icon": "terminal",
            "match_score": int(score),
            "key_skills": matched_in_track or ["Python"],
            "recommended_roles": roles,
            "description": "Backend API development, machine learning pipelines, data processing, and automation.",
        })
        all_recommended_roles.extend(roles[:2])

    # 3. Java Enterprise & Cloud Backend Track
    has_java = any(s in skills_lower for s in ("java", "spring boot", "hibernate", "maven", "microservices"))
    if has_java:
        matched_in_track = [s for s in matched_skills if s.lower() in ("java", "spring boot", "microservices", "sql", "docker", "rest apis", "git / github")]
        roles = [
            "Java Backend Developer",
            "Spring Boot Enterprise Engineer",
            "Java Software Developer",
            "Microservices Engineer",
        ]
        score = min(96, 75 + len(matched_in_track) * 6)
        tracks.append({
            "track_name": "Java Enterprise & Cloud Backend",
            "badge": "Java Enterprise",
            "icon": "coffee",
            "match_score": int(score),
            "key_skills": matched_in_track or ["Java"],
            "recommended_roles": roles,
            "description": "Enterprise-scale backend services, Spring Boot microservices, high-concurrency architectures.",
        })
        all_recommended_roles.extend(roles[:2])

    # 4. Full Stack & Modern Web Track
    has_web = any(s in skills_lower for s in ("javascript", "typescript", "react", "react.js", "node.js", "node", "html/css", "express.js", "next.js"))
    if has_web:
        matched_in_track = [s for s in matched_skills if s.lower() in ("javascript", "typescript", "react.js", "react", "node.js", "node", "html/css", "express.js", "mongodb", "rest apis")]
        roles = [
            "Full Stack Developer",
            "Frontend React Developer",
            "Node.js Backend Developer",
            "Web Application Engineer",
        ]
        score = min(96, 76 + len(matched_in_track) * 5)
        tracks.append({
            "track_name": "Full Stack & Web Engineering",
            "badge": "Full Stack Web",
            "icon": "globe",
            "match_score": int(score),
            "key_skills": matched_in_track or ["JavaScript", "React.js"],
            "recommended_roles": roles,
            "description": "End-to-end responsive web applications, modern interactive interfaces, and scalable REST APIs.",
        })
        all_recommended_roles.extend(roles[:2])

    # 5. Cloud & DevOps Track
    has_cloud = any(s in skills_lower for s in ("aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "linux / shell"))
    if has_cloud:
        matched_in_track = [s for s in matched_skills if s.lower() in ("aws", "azure", "google cloud (gcp)", "docker", "kubernetes", "terraform", "ci/cd", "linux / shell")]
        roles = [
            "Cloud Engineer",
            "DevOps Engineer",
            "Site Reliability Engineer",
            "Platform Engineer",
        ]
        score = min(96, 75 + len(matched_in_track) * 6)
        tracks.append({
            "track_name": "Cloud, Infrastructure & DevOps",
            "badge": "Cloud & DevOps",
            "icon": "cloud",
            "match_score": int(score),
            "key_skills": matched_in_track or ["AWS", "Docker"],
            "recommended_roles": roles,
            "description": "Cloud architecture, container orchestration, CI/CD pipelines, and infrastructure as code.",
        })
        all_recommended_roles.extend(roles[:2])

    # 6. Database & Data Analytics Track
    has_data = any(s in skills_lower for s in ("sql", "mysql", "postgresql", "mongodb", "power bi", "tableau", "data structures & algorithms"))
    if has_data and not any(t["badge"] == "Python & AI" for t in tracks):
        matched_in_track = [s for s in matched_skills if s.lower() in ("sql", "mysql", "postgresql", "mongodb", "power bi", "tableau", "data structures & algorithms")]
        roles = [
            "Data Analyst",
            "Database Administrator",
            "Business Intelligence Engineer",
            "SQL Developer",
        ]
        score = min(95, 74 + len(matched_in_track) * 5)
        tracks.append({
            "track_name": "Data Analytics & Database Management",
            "badge": "Data & Analytics",
            "icon": "database",
            "match_score": int(score),
            "key_skills": matched_in_track or ["SQL"],
            "recommended_roles": roles,
            "description": "Database query optimization, data warehousing, reporting dashboards, and business insights.",
        })
        all_recommended_roles.extend(roles[:2])

    # Default fallback track if non-tech or general profile
    if not tracks:
        profile = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["Information Technology"])
        default_roles = list(profile["roles"])
        tracks.append({
            "track_name": f"{domain} Career Track",
            "badge": domain,
            "icon": "briefcase",
            "match_score": 78,
            "key_skills": matched_skills[:5] or ["Core Competencies"],
            "recommended_roles": default_roles[:4],
            "description": f"Targeted career pathways aligned with {domain} professional proficiencies.",
        })
        all_recommended_roles.extend(default_roles[:4])

    # Deduplicate recommended roles
    deduped_roles: list[str] = []
    seen: set[str] = set()
    for r in all_recommended_roles:
        clean = r.strip()
        if clean.lower() not in seen:
            seen.add(clean.lower())
            deduped_roles.append(clean)

    return {
        "career_tracks": tracks,
        "recommended_roles": deduped_roles[:6],
    }


def calculate_score_breakdown(
    skills_score: int,
    experience_score: int,
    education_score: int,
    projects_activities_score: int,
) -> dict[str, Any]:
    """
    Calculate the 4-Pillar Score Breakdown and composite ATS Score.
    - Skills Weight: 35%
    - Experience Weight: 25%
    - Education & CGPA Weight: 20%
    - Projects & Activities Weight: 20%
    """
    overall = round(
        0.35 * skills_score +
        0.25 * experience_score +
        0.20 * education_score +
        0.20 * projects_activities_score
    )
    overall = max(20, min(98, overall))

    return {
        "overall_ats_score": int(overall),
        "skills_score": int(skills_score),
        "experience_score": int(experience_score),
        "education_score": int(education_score),
        "projects_activities_score": int(projects_activities_score),
        "weights": {
            "skills": "35%",
            "experience": "25%",
            "education": "20%",
            "projects_activities": "20%",
        },
    }


# ==============================================================================
# LEGACY & COMPATIBILITY HELPERS
# ==============================================================================

def detect_domain(text: str) -> str:
    lower = text.lower()
    scores: list[tuple[str, int]] = []
    for domain, profile in DOMAIN_PROFILES.items():
        if domain == "General / Fresher":
            continue
        hits = sum(1 for sig in profile["signals"] if sig in lower)
        scores.append((domain, hits))
    scores.sort(key=lambda item: item[1], reverse=True)
    if scores and scores[0][1] > 0:
        return scores[0][0]
    return "Information Technology"


def sanitize_skills(skills: list[str], metadata: dict[str, str]) -> list[str]:
    """
    Sanitizes extracted skills while preserving valid single/short skill names like C, C++, C#, R, Go.
    """
    email = (metadata.get("candidate_email") or "").lower()
    phone_digits = re.sub(r"\D", "", metadata.get("candidate_phone") or "")
    name = (metadata.get("candidate_name") or "").strip()
    name_parts = {p.lower() for p in name.split() if len(p) > 1}
    cleaned: list[str] = []
    seen: set[str] = set()

    for raw in skills:
        skill = str(raw).strip()
        if not skill:
            continue
        sl = skill.lower()
        if sl in seen or sl in _STOPWORDS or sl == "not found":
            continue
        if re.search(r"@|\.com|\.in|\.org", sl):
            continue
        if re.fullmatch(r"\+?[\d\s\-()]{7,}", skill):
            continue
        if email and email != "not found" and (email in sl or sl in email):
            continue
        skill_digits = re.sub(r"\D", "", sl)
        if phone_digits and len(phone_digits) >= 8 and phone_digits in skill_digits:
            continue
        tokens = [t for t in re.findall(r"[a-z]+", sl) if len(t) > 2]
        if name_parts and tokens and all(t in name_parts for t in tokens):
            continue
        if name and name.lower() == sl:
            continue
        # Allow 1-letter valid skills (C, R) and up to 48 chars
        if len(sl) > 48:
            continue
        if "," in skill and _looks_like_location_skill(skill):
            continue
        seen.add(sl)
        cleaned.append(skill)
    return cleaned[:30]


def _looks_like_location_skill(value: str) -> bool:
    lower = value.lower()
    markers = (
        "india", "bengaluru", "bangalore", "mumbai", "delhi", "chennai",
        "hyderabad", "pune", "kolkata", "karnataka", "street", "road",
    )
    return any(m in lower for m in markers)


def compute_missing_skills(matched: list[str], domain: str) -> list[str]:
    pool = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["Information Technology"])["skill_pool"]
    matched_lower = {m.lower() for m in matched}
    missing = [s for s in pool if s.lower() not in matched_lower]
    return missing[:8] if missing else pool[:4]


def infer_roles_from_skills(matched_skills: list[str], domain: str) -> list[str]:
    tracks_info = generate_multi_skill_career_tracks(matched_skills, {}, domain)
    return tracks_info["recommended_roles"]


def merge_recommended_roles(primary: list[str], skill_roles: list[str], limit: int = 6) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for role in primary + skill_roles:
        key = role.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        merged.append(role.strip())
        if len(merged) >= limit:
            break
    return merged


def extract_professional_skills(text: str, domain: str) -> list[str]:
    data = extract_comprehensive_skills(text)
    return data["all_skills"]
