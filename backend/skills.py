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
            "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud (GCP)", "Terraform",
            "CI/CD", "Linux / Shell", "Ansible", "Jenkins", "VPC & IAM", "Monitoring & Logging",
            "Microservices", "Helm", "Git / GitHub",
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
            "C++", "C#", "TypeScript", "Docker", "AWS", "Microservices", "Redis",
            "PostgreSQL", "Spring Boot", "FastAPI", "Data Structures & Algorithms",
            "CI/CD", "Next.js", "Kubernetes", "Linux / Shell", "GraphQL",
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
            "Embedded C", "C++", "FreeRTOS", "ARM Architecture", "Device Drivers",
            "Linux Kernel", "I2C / SPI / UART", "Socket Programming", "Microcontrollers",
            "Multithreading", "Debugging & GDB", "PCB Design Basics",
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
            "PyTorch", "TensorFlow", "Scikit-Learn", "Machine Learning", "Deep Learning",
            "NLP", "Computer Vision", "Data Visualization", "SQL", "Pandas",
            "NumPy", "MLOps", "Feature Engineering", "Statistical Modeling",
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
            "Cisco Networking", "TCP/IP & Subnetting", "Routing (BGP/OSPF)", "Wireshark",
            "Network Firewalls", "VLAN Configuration", "DNS / DHCP", "Network Security",
            "VPN Configuration", "CCNA Standards", "Linux Networking",
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
            "Financial Modeling", "Advanced MS Excel", "Tally ERP / Prime", "GST Compliance",
            "Financial Reporting", "Bank Reconciliation", "Taxation & TDS", "Budgeting & Forecasting",
            "Auditing Standards", "Cost Accounting",
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
            "Digital Marketing", "SEO & SEM", "Google Analytics", "Content Strategy",
            "CRM Management (HubSpot/Salesforce)", "Market Research", "Social Media Campaigns",
            "Operations & Supply Chain", "Performance Marketing",
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
            "Patient Care & Triage", "Clinical Documentation", "Medical Terminology",
            "Healthcare Compliance (NABH)", "Pharmacology Basics", "Vital Signs Monitoring",
            "Electronic Health Records (EHR)", "Infection Control",
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
            "Curriculum Planning", "Classroom Management", "Pedagogical Delivery",
            "Student Assessment", "EdTech Tools (LMS)", "Academic Counseling",
            "Public Speaking & Presentation",
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
            "Project Management (Agile/Scrum)", "Stakeholder Management", "Strategic Planning",
            "Team Leadership", "Business Analytics", "Risk Management",
            "Process Optimization", "Performance Management",
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
            "Professional Content Writing", "Editorial Review & Copywriting", "Research Methodology",
            "Public Relations & Communications", "Brand Storytelling", "Social Media Management",
            "Creative Problem Solving",
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
            "Advanced MS Office / Google Workspace", "Executive Scheduling", "Office Operations",
            "Business Correspondence", "Records & Database Management", "Vendor Coordination",
            "Customer Relationship Management",
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
            "AutoCAD 2D/3D", "SolidWorks / CATIA", "MATLAB & Simulink", "Quality Control (Six Sigma)",
            "Technical Documentation", "Engineering Standards (ISO/ASME)", "Root Cause Analysis",
            "Finite Element Analysis (FEA)",
        ],
    },
    "General / Fresher": {
        "signals": ("fresher", "graduate", "intern", "trainee", "entry level", "bachelor"),
        "roles": [
            "Graduate Trainee", "Management Trainee", "Junior Executive",
            "Customer Support Associate", "Operations Trainee",
        ],
        "skill_pool": [
            "Professional Communication", "MS Office / Excel", "Critical Problem Solving",
            "Project Coordination", "Time Management", "Presentation Skills",
            "Analytical Thinking",
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
    (".net", re.compile(r"(?<![a-zA-Z0-9])(?:\.net|dotnet|asp\.net)\b", re.IGNORECASE), ".NET"),
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
# NEGATION DETECTION FOR EVIDENCE-BASED SKILL EXTRACTION
# Prevents false positives from claims like "No practical Kubernetes experience"
# ==============================================================================
_NEGATION_PREFIXES = re.compile(
    r"\b(?:no|not|none|never|lack|lacks|lacking|lacked|without|haven't|hasn't|hadn't|"
    r"have\s+not|has\s+not|had\s+not|zero|little\s+to\s+no|minimal\s+to\s+no|exclude|excluding|"
    r"unfamiliar\s+with|no\s+practical|no\s+prior|no\s+hands-on|"
    r"not\s+experienced\s+(?:in|with)|not\s+familiar\s+with|no\s+experience\s+(?:with|in)|"
    r"limited\s+to\s+no|no\s+knowledge\s+of|haven't\s+used|have\s+not\s+used)\b",
    re.IGNORECASE,
)


def _is_negated_match(text: str, match_start: int, window: int = 60) -> bool:
    """
    Check if a matched skill term is preceded by a negation indicator within the same clause.
    """
    prefix = text[max(0, match_start - window):match_start]
    clause = re.split(r"[.;\n!?]", prefix)[-1]
    return bool(_NEGATION_PREFIXES.search(clause))


def _has_positive_evidence(pat: re.Pattern, text: str) -> bool:
    """
    Returns True only if at least one match of pattern in text is free of negative context.
    If every mention in the resume is negated, returns False.
    """
    matches = list(pat.finditer(text))
    if not matches:
        return False
    return any(not _is_negated_match(text, m.start()) for m in matches)


# ==============================================================================
# DOMAIN-SPECIFIC PROFESSIONAL COMPETENCY PATTERNS
# Ensures fair skill detection for Non-IT domains (Commerce, Healthcare, Education, etc.)
# ==============================================================================
DOMAIN_SPECIFIC_PATTERNS: dict[str, list[tuple[str, re.Pattern, str]]] = {
    "Commerce & Finance": [
        ("tally", re.compile(r"\b(?:tally|tally\s*(?:erp|prime|9))\b", re.IGNORECASE), "Tally ERP / Prime"),
        ("gst", re.compile(r"\b(?:gst|goods\s+and\s+services\s+tax|gst\s+filing)\b", re.IGNORECASE), "GST Compliance"),
        ("financial modeling", re.compile(r"\bfinancial\s+model(?:ing)?\b", re.IGNORECASE), "Financial Modeling"),
        ("auditing", re.compile(r"\b(?:audit(?:ing)?|statutory\s+audit|internal\s+audit)\b", re.IGNORECASE), "Auditing Standards"),
        ("taxation", re.compile(r"\b(?:tax(?:ation)?|direct\s+tax|indirect\s+tax|tds|income\s+tax)\b", re.IGNORECASE), "Taxation & TDS"),
        ("reconciliation", re.compile(r"\b(?:bank\s+reconciliation|account\s+reconciliation)\b", re.IGNORECASE), "Bank Reconciliation"),
        ("financial reporting", re.compile(r"\bfinancial\s+report(?:ing|s)?\b", re.IGNORECASE), "Financial Reporting"),
        ("excel", re.compile(r"\b(?:advanced\s+excel|ms\s*excel|vlookup|pivot\s*tables?)\b", re.IGNORECASE), "Advanced MS Excel"),
    ],
    "Healthcare": [
        ("patient care", re.compile(r"\bpatient\s+care\b", re.IGNORECASE), "Patient Care & Triage"),
        ("clinical doc", re.compile(r"\bclinical\s+doc(?:umentation)?\b", re.IGNORECASE), "Clinical Documentation"),
        ("ehr", re.compile(r"\b(?:ehr|emr|electronic\s+health\s+records?)\b", re.IGNORECASE), "Electronic Health Records (EHR)"),
        ("medical terms", re.compile(r"\bmedical\s+terminolog(?:y|ies)\b", re.IGNORECASE), "Medical Terminology"),
        ("pharmacology", re.compile(r"\bpharmacol(?:ogy|ogical)\b", re.IGNORECASE), "Pharmacology Basics"),
        ("infection control", re.compile(r"\binfection\s+control\b", re.IGNORECASE), "Infection Control"),
        ("vital signs", re.compile(r"\bvital\s+signs?(?:\s+monitoring)?\b", re.IGNORECASE), "Vital Signs Monitoring"),
    ],
    "Education": [
        ("curriculum", re.compile(r"\bcurriculum(?:\s+planning|\s+design)?\b", re.IGNORECASE), "Curriculum Planning"),
        ("classroom mgmt", re.compile(r"\bclassroom\s+management\b", re.IGNORECASE), "Classroom Management"),
        ("pedagogy", re.compile(r"\b(?:pedagog(?:y|ical)|lesson\s+planning)\b", re.IGNORECASE), "Pedagogical Delivery"),
        ("lms", re.compile(r"\b(?:lms|learning\s+management\s+systems?|moodle|canvas)\b", re.IGNORECASE), "EdTech Tools (LMS)"),
        ("counseling", re.compile(r"\bacademic\s+counsel(?:ing)?\b", re.IGNORECASE), "Academic Counseling"),
        ("assessment", re.compile(r"\bstudent\s+assessment\b", re.IGNORECASE), "Student Assessment"),
    ],
    "Core Engineering": [
        ("autocad", re.compile(r"\bautocad(?:\s*2d|\s*3d)?\b", re.IGNORECASE), "AutoCAD 2D/3D"),
        ("solidworks", re.compile(r"\b(?:solidworks|catia|creo|inventor)\b", re.IGNORECASE), "SolidWorks / CATIA"),
        ("matlab", re.compile(r"\b(?:matlab|simulink)\b", re.IGNORECASE), "MATLAB & Simulink"),
        ("fea", re.compile(r"\b(?:fea|ansys|finite\s+element)\b", re.IGNORECASE), "Finite Element Analysis (FEA)"),
        ("six sigma", re.compile(r"\b(?:six\s+sigma|quality\s+control|qc|qa/qc)\b", re.IGNORECASE), "Quality Control (Six Sigma)"),
        ("root cause", re.compile(r"\broot\s+cause\s+analysis\b|\brca\b", re.IGNORECASE), "Root Cause Analysis"),
    ],
    "Marketing & Operations": [
        ("digital marketing", re.compile(r"\bdigital\s+marketing\b", re.IGNORECASE), "Digital Marketing"),
        ("seo", re.compile(r"\b(?:seo|search\s+engine\s+optimization)\b", re.IGNORECASE), "SEO & SEM"),
        ("sem", re.compile(r"\b(?:sem|google\s+ads|ppc)\b", re.IGNORECASE), "Performance Marketing"),
        ("analytics", re.compile(r"\bgoogle\s+analytics\b|\bga4\b", re.IGNORECASE), "Google Analytics"),
        ("crm", re.compile(r"\b(?:crm|hubspot|salesforce|zoho\s+crm)\b", re.IGNORECASE), "CRM Management (HubSpot/Salesforce)"),
        ("content strategy", re.compile(r"\bcontent\s+strateg(?:y|ies)\b", re.IGNORECASE), "Content Strategy"),
        ("supply chain", re.compile(r"\b(?:supply\s+chain|logistics|inventory\s+management)\b", re.IGNORECASE), "Operations & Supply Chain"),
    ],
    "Embedded & Systems Engineering": [
        ("embedded c", re.compile(r"\bembedded\s+c\b", re.IGNORECASE), "Embedded C"),
        ("freertos", re.compile(r"\b(?:freertos|rtos)\b", re.IGNORECASE), "FreeRTOS"),
        ("arm", re.compile(r"\b(?:arm|cortex-m|stm32)\b", re.IGNORECASE), "ARM Architecture"),
        ("protocols", re.compile(r"\b(?:i2c|spi|uart|can\s+bus)\b", re.IGNORECASE), "I2C / SPI / UART"),
        ("microcontrollers", re.compile(r"\b(?:microcontrollers?|arduino|esp32|pic|raspberry\s*pi)\b", re.IGNORECASE), "Microcontrollers"),
        ("device drivers", re.compile(r"\bdevice\s+drivers?\b", re.IGNORECASE), "Device Drivers"),
    ],
    "Network Engineering": [
        ("cisco", re.compile(r"\b(?:cisco|ccna|ccnp)\b", re.IGNORECASE), "Cisco Networking"),
        ("tcp/ip", re.compile(r"\btcp/ip\b|\bsubnetting\b", re.IGNORECASE), "TCP/IP & Subnetting"),
        ("routing", re.compile(r"\b(?:routing|switching|bgp|ospf)\b", re.IGNORECASE), "Routing (BGP/OSPF)"),
        ("wireshark", re.compile(r"\bwireshark\b", re.IGNORECASE), "Wireshark"),
        ("firewall", re.compile(r"\b(?:firewalls?|palo\s*alto|fortinet|checkpoint)\b", re.IGNORECASE), "Network Firewalls"),
        ("vlan", re.compile(r"\bvlan(?:s)?\b", re.IGNORECASE), "VLAN Configuration"),
        ("dns/dhcp", re.compile(r"\b(?:dns|dhcp)\b", re.IGNORECASE), "DNS / DHCP"),
    ],
    "Management": [
        ("project mgmt", re.compile(r"\bproject\s+management\b|\bscrum\b|\bagile\b", re.IGNORECASE), "Project Management (Agile/Scrum)"),
        ("stakeholder", re.compile(r"\bstakeholder\s+management\b", re.IGNORECASE), "Stakeholder Management"),
        ("strategic planning", re.compile(r"\bstrategic\s+planning\b", re.IGNORECASE), "Strategic Planning"),
        ("risk mgmt", re.compile(r"\brisk\s+management\b", re.IGNORECASE), "Risk Management"),
        ("process opt", re.compile(r"\bprocess\s+optimization\b|\bprocess\s+improvement\b", re.IGNORECASE), "Process Optimization"),
    ],
}


# ==============================================================================
# COMPREHENSIVE MULTI-DIMENSIONAL EXTRACTION FUNCTIONS
# ==============================================================================

def extract_comprehensive_skills(text: str, domain: str | None = None) -> dict[str, Any]:
    """
    Extract all skills cleanly without omitting short or symbol-based skills (C, C++, C#, Java, Python, etc.)
    Validates evidence and filters out negative claims (e.g. 'no practical experience with X').
    """
    languages: list[str] = []
    frameworks: list[str] = []
    cloud_devops: list[str] = []
    databases: list[str] = []
    tools: list[str] = []
    soft_skills: list[str] = []
    domain_skills: list[str] = []
    all_matched: list[str] = []
    seen_lower: set[str] = set()

    def add_skill(cat_list: list[str], canonical: str):
        low = canonical.lower()
        if low not in seen_lower:
            seen_lower.add(low)
            cat_list.append(canonical)
            all_matched.append(canonical)

    for _, pat, name in LANGUAGE_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(languages, name)

    for _, pat, name in FRAMEWORK_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(frameworks, name)

    for _, pat, name in CLOUD_DEVOPS_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(cloud_devops, name)

    for _, pat, name in DATABASE_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(databases, name)

    for _, pat, name in TOOL_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(tools, name)

    for _, pat, name in SOFT_SKILL_PATTERNS:
        if _has_positive_evidence(pat, text):
            add_skill(soft_skills, name)

    # Detect domain if not provided
    active_domain = domain or detect_domain(text)
    if active_domain in DOMAIN_SPECIFIC_PATTERNS:
        for _, pat, name in DOMAIN_SPECIFIC_PATTERNS[active_domain]:
            if _has_positive_evidence(pat, text):
                add_skill(domain_skills, name)

    return {
        "languages": languages,
        "frameworks": frameworks,
        "cloud_devops": cloud_devops,
        "databases": databases,
        "tools": tools,
        "soft_skills": soft_skills,
        "domain_skills": domain_skills,
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


_SKILL_KEY_MAP = {
    "react": "react",
    "react.js": "react",
    "reactjs": "react",
    "node": "node",
    "node.js": "node",
    "nodejs": "node",
    "express": "express",
    "express.js": "express",
    "expressjs": "express",
    "next": "nextjs",
    "next.js": "nextjs",
    "nextjs": "nextjs",
    "git": "git",
    "github": "git",
    "git / github": "git",
    "git/github": "git",
    "c++": "cpp",
    "cpp": "cpp",
    "c#": "csharp",
    "csharp": "csharp",
    "c": "c",
    "aws": "aws",
    "amazon web services": "aws",
    "gcp": "gcp",
    "google cloud": "gcp",
    "google cloud (gcp)": "gcp",
    "azure": "azure",
    "microsoft azure": "azure",
    "html": "htmlcss",
    "css": "htmlcss",
    "html/css": "htmlcss",
    "html5": "htmlcss",
    "css3": "htmlcss",
    "postgresql": "postgres",
    "postgres": "postgres",
    "sql": "sql",
    "mysql": "mysql",
    "dsa": "dsa",
    "data structures": "dsa",
    "algorithms": "dsa",
    "data structures & algorithms": "dsa",
    "rest api": "restapi",
    "rest apis": "restapi",
    "restful apis": "restapi",
    "api": "restapi",
    "docker": "docker",
    "kubernetes": "k8s",
    "k8s": "k8s",
    "ci/cd": "cicd",
    "cicd": "cicd",
    "linux": "linux",
    "linux / shell": "linux",
    "spring boot": "springboot",
    "springboot": "springboot",
    "fastapi": "fastapi",
    "django": "django",
    "flask": "flask",
    "mongodb": "mongodb",
    "redis": "redis",
    "typescript": "typescript",
    "javascript": "javascript",
    "python": "python",
    "java": "java",
}

_RELATED_SKILL_GROUPS: list[set[str]] = [
    {"react.js", "next.js", "vue.js", "angular", "javascript", "typescript", "html/css", "node.js"},
    {"python", "django", "fastapi", "flask"},
    {"docker", "kubernetes", "terraform", "ansible", "ci/cd", "aws", "azure", "google cloud (gcp)", "linux / shell"},
    {"postgresql", "mysql", "mongodb", "redis", "oracle db", "sql"},
    {"java", "spring boot", "microservices"},
    {"c", "c++", "embedded c", "freertos", "arm architecture"},
    {"machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "nlp", "computer vision", "pandas", "numpy"},
    {"tally erp / prime", "gst compliance", "financial reporting", "taxation & tds", "bank reconciliation", "auditing standards"},
    {"autocad 2d/3d", "solidworks / catia", "matlab & simulink", "finite element analysis (fea)"},
    {"cisco networking", "tcp/ip & subnetting", "routing (bgp/ospf)", "wireshark", "network firewalls"},
    {"digital marketing", "seo & sem", "google analytics", "performance marketing"},
    {"patient care & triage", "clinical documentation", "electronic health records (ehr)", "infection control"},
]


def _skill_normalized_key(skill_name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9+#/]", "", skill_name.lower().strip())
    if skill_name.lower().strip() in _SKILL_KEY_MAP:
        return _SKILL_KEY_MAP[skill_name.lower().strip()]
    if cleaned in _SKILL_KEY_MAP:
        return _SKILL_KEY_MAP[cleaned]
    return cleaned


def compute_missing_skills(matched: list[str], domain: str) -> list[str]:
    pool = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["Information Technology"])["skill_pool"]
    matched_keys = {_skill_normalized_key(m) for m in matched if m}
    missing: list[str] = []
    seen_keys: set[str] = set()

    for s in pool:
        k = _skill_normalized_key(s)
        if k not in matched_keys and k not in seen_keys:
            seen_keys.add(k)
            missing.append(s)

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


def extract_professional_skills(text: str, domain: str = "Information Technology") -> list[str]:
    data = extract_comprehensive_skills(text, domain=domain)
    return data["all_skills"]


def evaluate_ats_score(
    text: str,
    domain: str = "Information Technology",
    job_description: str | None = None,
) -> dict[str, Any]:
    """
    Transparent, explainable ATS evaluation engine adhering to 4 distinct concepts:
    1. General Resume Quality Score (Structure, Readability, Action Impact, Completeness)
    2. Domain Competency Coverage Score (Evidenced Skills vs Domain/Target Role Benchmark)
    3. Evidence & Practical Application Score (Projects, Certifications, Experience Evidence)
    4. Optional Job-Specific Compatibility Score (when job_description is provided)

    Weights:
    - Without Job Description:
        * General Quality: 30%
        * Skill Coverage: 40%
        * Practical Evidence: 30%
    - With Job Description:
        * General Quality: 25%
        * Skill Coverage: 25%
        * Practical Evidence: 20%
        * Job Compatibility: 30%
    """
    lower = text.lower()

    # 1. Structural section presence
    section_map = {
        "contact_info": bool(re.search(r"@|\b(?:\+91[\-\s]?)?[6-9]\d{9}\b", text)),
        "summary_objective": bool(re.search(r"\b(summary|objective|profile|about\s+me)\b", lower)),
        "experience": bool(re.search(r"\b(experience|work\s+history|employment|internship|roles?)\b", lower)),
        "education": bool(re.search(r"\b(education|academic|b\.tech|b\.e|degree|college|university)\b", lower)),
        "skills": bool(re.search(r"\b(skills|technical\s+skills|core\s+competencies|technologies)\b", lower)),
        "projects_certs": bool(re.search(r"\b(projects?|certifications?|certificates?|activities|achievements)\b", lower)),
    }
    sections_present = [sec for sec, present in section_map.items() if present]
    section_score = round((len(sections_present) / len(section_map)) * 100)

    # 2. Action verbs and measurable impact
    action_verbs = [
        "led", "designed", "developed", "architected", "deployed", "scaled", "optimized",
        "managed", "implemented", "built", "spearheaded", "engineered", "collaborated",
        "created", "achieved", "reduced", "increased", "delivered", "resolved"
    ]
    action_hits = sum(1 for v in action_verbs if re.search(rf"\b{v}\b", lower))
    action_score = min(100, max(30, 40 + action_hits * 6))

    # Metrics detection (numbers, %, $, x times)
    metric_matches = re.findall(
        r"\b\d+(?:\.\d+)?%|\b\d+\s*(?:k|m|million|users|clients|requests|transactions)\b|\b\d+\+?\s*(?:years?|months?)\b",
        lower,
    )
    metrics_count = len(metric_matches)
    metrics_score = min(100, max(35, 45 + metrics_count * 10))

    # General Quality composite (sections 40%, action verbs 30%, metrics/readability 30%)
    general_quality = round(0.40 * section_score + 0.30 * action_score + 0.30 * metrics_score)
    general_quality = max(25, min(98, general_quality))

    # 3. Domain Competency Coverage
    skills_data = extract_comprehensive_skills(text, domain=domain)
    evidenced_skills = skills_data["all_skills"]
    profile = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["Information Technology"])
    skill_pool = profile.get("skill_pool", [])

    # Coverage normalized for career depth (freshers/non-tech not penalized)
    target_benchmark = min(8, len(skill_pool)) if len(skill_pool) > 0 else 6
    coverage_ratio = len(evidenced_skills) / max(1, target_benchmark)
    skill_coverage = min(98, max(30, round(35 + coverage_ratio * 60)))

    # 4. Evidence & Practical Application
    exp_details = extract_experience_details(text)
    proj_details = extract_projects_and_activities(text)

    practical_evidence = round(
        0.50 * proj_details["projects_activities_score"] +
        0.50 * exp_details["experience_score"]
    )
    practical_evidence = max(25, min(98, practical_evidence))

    # 5. Job-Specific Compatibility (if job_description provided)
    job_compatibility = None
    jd_matched: list[str] = []
    jd_missing: list[str] = []
    explicitly_demonstrated: list[str] = []
    potentially_demonstrated: list[str] = []
    not_found: list[str] = []
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    jd_analysis: dict[str, Any] | None = None

    if job_description and job_description.strip():
        jd_skills_data = extract_comprehensive_skills(job_description, domain=domain)
        jd_skills = jd_skills_data["all_skills"]
        resume_keys = {_skill_normalized_key(s) for s in evidenced_skills}
        resume_skills_lower = {s.lower() for s in evidenced_skills}

        jd_lower = job_description.lower()
        preferred_markers = ("preferred", "plus", "nice to have", "good to have", "bonus", "desired", "advantageous")

        for s in jd_skills:
            s_low = s.lower()
            is_pref = False
            for marker in preferred_markers:
                idx = jd_lower.find(marker)
                if idx != -1:
                    snippet = jd_lower[max(0, idx - 40):min(len(jd_lower), idx + 140)]
                    if s_low in snippet:
                        is_pref = True
                        break
            if is_pref:
                preferred_skills.append(s)
            else:
                required_skills.append(s)

            if _skill_normalized_key(s) in resume_keys or s_low in resume_skills_lower:
                explicitly_demonstrated.append(s)
                jd_matched.append(s)
            else:
                is_related = False
                for group in _RELATED_SKILL_GROUPS:
                    if s_low in group and any(res_s in group for res_s in resume_skills_lower):
                        is_related = True
                        break
                if is_related:
                    potentially_demonstrated.append(s)
                    jd_missing.append(s)
                else:
                    not_found.append(s)
                    jd_missing.append(s)

        jd_exp_match = re.search(r"\b(\d+)\+?\s*(?:-\s*\d+)?\s*years?(?:\s+of)?\s+experience\b", jd_lower)
        jd_exp_years = int(jd_exp_match.group(1)) if jd_exp_match else None
        cand_exp_years = exp_details.get("total_years", 0)

        # Token overlap
        r_tokens = set(re.findall(r"\b[a-zA-Z0-9+#]{2,}\b", lower))
        j_tokens = set(re.findall(r"\b[a-zA-Z0-9+#]{2,}\b", jd_lower))
        token_sim = (len(r_tokens & j_tokens) / len(j_tokens)) * 100 if j_tokens else 60.0

        matched_weight = len(explicitly_demonstrated) + 0.45 * len(potentially_demonstrated)
        skill_match_ratio = matched_weight / max(1, len(jd_skills)) if jd_skills else 0.7
        job_compatibility = round(0.65 * (skill_match_ratio * 100) + 0.35 * token_sim)
        job_compatibility = max(20, min(98, job_compatibility))

        jd_analysis = {
            "matched_requirements": jd_matched,
            "missing_requirements": jd_missing,
            "explicitly_demonstrated": explicitly_demonstrated,
            "potentially_demonstrated": potentially_demonstrated,
            "not_found": not_found,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "experience_requirement": f"{jd_exp_years}+ years" if jd_exp_years else "Not strictly specified",
            "candidate_experience": f"{cand_exp_years} years evidenced" if cand_exp_years else "Entry-level / Early-career",
            "evidence_note": "A missing mention in the resume is not proof that the candidate lacks the skill.",
        }

    # Evidence-based explanations
    evidence_explanations: list[str] = []
    evidence_explanations.append(
        f"Detected {len(evidenced_skills)} professional competencies verified from resume text ({', '.join(evidenced_skills[:5]) or 'foundational skills'})."
    )
    if action_hits >= 4:
        evidence_explanations.append(
            f"Strong action orientation with {action_hits}+ impact verbs highlighting direct engineering and operational contributions."
        )
    else:
        evidence_explanations.append(
            "Recommendation: Incorporate more active verbs (e.g., 'architected', 'optimized', 'led') to strengthen impact."
        )
    if metrics_count >= 2:
        evidence_explanations.append(
            f"Quantifiable results identified across {metrics_count} achievements (percentages, timeframes, or scale metrics)."
        )
    else:
        evidence_explanations.append(
            "Recommendation: Add quantified outcomes (e.g. '% speedup', 'team size', 'volume processed') to bullet points."
        )
    if len(sections_present) >= 5:
        evidence_explanations.append(
            f"High structural completeness across {len(sections_present)} standard resume sections."
        )
    if job_compatibility is not None:
        evidence_explanations.append(
            f"Job Alignment: {len(explicitly_demonstrated)} skills explicitly demonstrated, {len(potentially_demonstrated)} related skills requiring review, {len(not_found)} not mentioned."
        )

    # Compute overall score
    if job_compatibility is not None:
        overall = round(
            0.25 * general_quality +
            0.25 * skill_coverage +
            0.20 * practical_evidence +
            0.30 * job_compatibility
        )
        weights = {
            "general_quality": "25%",
            "skill_coverage": "25%",
            "practical_evidence": "20%",
            "job_compatibility": "30%",
        }
    else:
        overall = round(
            0.30 * general_quality +
            0.40 * skill_coverage +
            0.30 * practical_evidence
        )
        weights = {
            "general_quality": "30%",
            "skill_coverage": "40%",
            "practical_evidence": "30%",
        }

    overall = max(20, min(98, overall))

    return {
        "overall_ats_score": int(overall),
        "general_quality_score": int(general_quality),
        "skill_coverage_score": int(skill_coverage),
        "practical_evidence_score": int(practical_evidence),
        "job_compatibility_score": int(job_compatibility) if job_compatibility is not None else None,
        "evidenced_skills": evidenced_skills,
        "sections_present": sections_present,
        "action_verbs_count": action_hits,
        "metrics_count": metrics_count,
        "scoring_weights": weights,
        "evidence_explanations": evidence_explanations,
        "job_specific_analysis": jd_analysis,
        "disclaimer": "This score is an internal compatibility estimate based on structural and skill heuristics, not an official ATS score or guarantee of hiring.",
    }
