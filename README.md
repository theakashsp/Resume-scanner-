# Resume Analyzer

**Resume Analyzer** is a full-stack career intelligence platform that scores resumes, extracts skills from real PDF content, maps realistic target roles, and surfaces live India job openings. Analysis is driven by the exact text extracted from each uploaded resume — not generic templates.

---

## Core Features

| Feature | Description |
| --- | --- |
| **ATS Scoring** | Domain-aware ATS score (0–100) calibrated to resume content |
| **Dynamic Skill Extraction** | Skills pulled only from evidenced resume text; PII and contact noise filtered out |
| **Realistic Role Matching** | Target roles matched to actual experience depth (fresher, non-IT, IT, cloud, commerce, etc.) |
| **Skill Gap Analysis** | Missing competencies identified relative to the candidate's target role |
| **Learning Roadmap** | Step-by-step milestones in the dashboard PDF report |
| **Live Job Matches** | 4 India openings per recommended role via JSearch (RapidAPI) or Adzuna |
| **PDF Career Report** | Branded export with profile, skills, roadmap, and clickable **Apply** links |
| **Multi-Domain Support** | IT, Cloud & DevOps, Network, Commerce, Healthcare, Education, Management, and more |

---

## System Architecture

```text
[ User ]
   │
   ▼  Upload PDF resume

┌─────────────────────────────┐
│   React Frontend            │
│   Resume Analyzer UI        │
│   Dashboard + PDF Export    │
└──────────────▲──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   FastAPI Backend           │
│   PDF parse · AI analyze    │
│   Job fetch · Stats API     │
└──────────────┬──────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
 Google Gemini      JSearch / Adzuna
 (resume analysis)  (live India jobs)
```

---

## Tech Stack

| Layer | Technologies |
| --- | --- |
| **Frontend** | React, Axios, jsPDF, jspdf-autotable, lucide-react, react-dropzone |
| **Backend** | Python, FastAPI, Uvicorn, Pydantic, Requests |
| **PDF Parsing** | pdfminer.six, pypdf (multi-method extraction) |
| **AI** | Google Gemini 2.5 Flash (`google-genai`) |
| **Jobs** | JSearch via RapidAPI, Adzuna India API |

---

## Quick Start

From the project root:

```bash
# Windows (Git Bash)
bash quick-start.sh

# Windows (CMD)
quick-start.bat
```

This will:

1. Create the Python virtual environment (if needed)
2. Install frontend dependencies (if needed)
3. Build the frontend (first run only)
4. Start the API on `http://127.0.0.1:8000`
5. Serve the app on `http://localhost:3000`

---

## Manual Setup

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Copy the environment template and add your keys:

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=your_gemini_api_key
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=jsearch.p.rapidapi.com

# Optional — Adzuna India jobs
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

> **Never commit `backend/.env`.** API keys stay local only. Copy `.env.example`, add your keys locally, and keep secrets out of version control.

Start the API:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

**Fast production mode** (pre-built bundle, ~5s startup):

```bash
npm run build:quick
npm run start:quick
```

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Service health and job provider status |
| `GET` | `/api/platform-stats` | Analysis counts and platform metrics |
| `GET` | `/api/features` | Feature list for the landing page |
| `POST` | `/analyze` | Upload PDF resume (multipart field: `file`) |
| `POST` | `/api/fetch-jobs` | Fetch live jobs for recommended roles |

Interactive docs: `http://127.0.0.1:8000/docs`

---

## Analysis Workflow

1. User uploads a PDF resume
2. Backend extracts text via pdfminer.six / pypdf
3. Resume validity is checked (rejects non-resume documents)
4. Gemini analyzes **only** the extracted resume text:
   - `candidate_domain`
   - `target_role` (realistic to experience depth)
   - `current_skills` (explicitly stated in resume)
   - `missing_skills` (gaps for the target role)
   - `custom_roadmap` (step-by-step milestones)
   - `ats_score`
5. Live India jobs are fetched per recommended role
6. Results appear on the dashboard; career roadmap and suggestions are included in the downloadable PDF

---

## PDF Report

The **Download Career Report** button generates a styled PDF including:

- Candidate profile (name, email, phone, college)
- ATS score with color-coded badge
- Domain, target role, and recommended roles
- Matched skills and skill gaps
- Career suggestions and learning roadmap
- Live job table with clickable **Apply** links

---

## Project Structure

```text
Resume-scanner--main/
├── backend/
│   ├── main.py              # FastAPI app, analyze route, job APIs
│   ├── skills.py            # Domain profiles, skill extraction
│   ├── pdf_parser.py        # Multi-method PDF text extraction
│   ├── report_generator.py  # Server-side PDF helper
│   ├── .env.example         # Environment template (no secrets)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main UI and dashboard
│   │   ├── pdfReport.js     # Client-side PDF generator
│   │   ├── TechBackground.js
│   │   └── LiveJobOpenings.js
│   └── package.json
├── quick-start.sh
├── quick-start.bat
└── README.md
```

---

## Deployment Tips

- Host the backend on **Render**, **Railway**, or **AWS**
- Deploy the frontend on **Vercel** or **Netlify**
- Set environment variables in the hosting dashboard — do not commit `.env`
- Point `REACT_APP_API_URL` to your deployed API URL for production builds

---

## License

This project is licensed under the **MIT License**.

---

## Support

If this project helped you, consider giving it a star on GitHub.
