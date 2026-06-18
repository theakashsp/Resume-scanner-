from fpdf import FPDF
from datetime import datetime


class PDFReport(FPDF):
    def header(self):
        self.set_fill_color(6, 6, 11)
        self.rect(0, 0, 210, 36, "F")
        self.set_fill_color(124, 58, 237)
        self.rect(0, 34, 210, 2, "F")
        self.set_text_color(6, 182, 212)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 8, "RESUME", ln=1, align="L")
        self.set_x(10)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "ANALYZER", ln=1, align="L")
        self.set_x(10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(200, 210, 230)
        self.cell(0, 6, "Career Intelligence Report", ln=1, align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(
            0,
            8,
            f"Resume Analyzer | Page {self.page_no()} | {datetime.now().strftime('%d %b %Y')}",
            align="C",
        )


def generate_pdf_report(data: dict, output_filepath: str):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)

    predicted_role = data.get("predicted_role") or data.get("target_role") or "Unknown Role"
    ats_score = int(data.get("ats_score") or 0)
    extracted_skills = data.get("matched_skills") or data.get("current_skills") or data.get("extracted_skills") or []
    missing_skills = data.get("missing_skills") or []
    domain = data.get("detected_domain") or data.get("candidate_domain") or "Not specified"
    name = data.get("candidate_name") or "Not found"
    email = data.get("candidate_email") or "Not found"
    phone = data.get("candidate_phone") or "Not found"
    college = data.get("candidate_college") or "Not found"
    suggestions = data.get("career_suggestions") or data.get("custom_suggestion") or ""
    roadmap = data.get("custom_roadmap") or data.get("learning_roadmap") or []
    jobs_by_role = data.get("jobs_by_role") or {}

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 8, "Candidate Profile", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    for label, value in [
        ("Name", name),
        ("Email", email),
        ("Phone", phone),
        ("College", college),
        ("Domain", domain),
        ("Target Role", predicted_role),
        ("ATS Score", f"{ats_score}/100"),
    ]:
        pdf.cell(0, 6, f"{label}: {value}", ln=1)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 8, "Matched Skills", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, ", ".join(str(s) for s in extracted_skills) or "None detected.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Skill Gaps", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, ", ".join(str(s) for s in missing_skills) or "No major gaps listed.")
    pdf.ln(2)

    if suggestions:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Career Suggestions", ln=1)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, suggestions)
        pdf.ln(2)

    if roadmap:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Learning Roadmap", ln=1)
        pdf.set_font("Helvetica", "", 10)
        for index, item in enumerate(roadmap, start=1):
            line = item if isinstance(item, str) else str(item.get("focus") or item.get("title") or "")
            if line:
                pdf.multi_cell(0, 6, f"{index}. {line}")
        pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Live Job Openings (India)", ln=1)
    pdf.set_font("Helvetica", "", 9)
    has_jobs = False
    for role_name, jobs in jobs_by_role.items():
        for job in jobs or []:
            has_jobs = True
            title = job.get("job_title") or "Open Role"
            company = job.get("company_name") or job.get("employer_name") or "Company"
            location = job.get("location") or "India"
            url = job.get("redirect_url") or job.get("job_apply_link") or ""
            pdf.multi_cell(0, 5, f"{role_name} | {company} | {title} | {location}")
            if url and url != "#":
                pdf.set_text_color(124, 58, 237)
                pdf.cell(0, 5, "Apply", link=url, ln=1)
                pdf.set_text_color(100, 116, 139)
            else:
                pdf.cell(0, 5, "Apply link unavailable", ln=1)
            pdf.ln(1)
    if not has_jobs:
        pdf.cell(0, 6, "No active listings found for your roles.", ln=1)

    pdf.output(output_filepath)
