import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

const COLORS = {
  bg: [6, 6, 11],
  surface: [248, 250, 252],
  purple: [124, 58, 237],
  cyan: [6, 182, 212],
  slate: [51, 65, 85],
  muted: [100, 116, 139],
  white: [255, 255, 255],
  green: [16, 185, 129],
  amber: [245, 158, 11],
  red: [239, 68, 68],
};

function scoreColor(score) {
  if (score >= 75) return COLORS.green;
  if (score >= 50) return COLORS.amber;
  return COLORS.red;
}

function drawHeaderBanner(doc) {
  doc.setFillColor(...COLORS.bg);
  doc.rect(0, 0, 210, 42, 'F');
  doc.setFillColor(...COLORS.purple);
  doc.rect(0, 40, 210, 2, 'F');

  doc.setTextColor(...COLORS.cyan);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.text('RESUME', 14, 14);

  doc.setTextColor(...COLORS.white);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(22);
  doc.text('ANALYZER', 14, 26);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(200, 210, 230);
  doc.text('Career Intelligence Report', 14, 34);

  const dateStr = new Date().toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
  doc.setFontSize(9);
  doc.text(dateStr, 196, 14, { align: 'right' });
}

function drawSectionTitle(doc, y, title, subtitle) {
  doc.setFillColor(...COLORS.purple);
  doc.rect(14, y - 4, 3, 10, 'F');
  doc.setTextColor(...COLORS.slate);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(12);
  doc.text(title, 20, y + 3);
  if (subtitle) {
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(...COLORS.muted);
    doc.text(subtitle, 20, y + 9);
    return y + 14;
  }
  return y + 8;
}

function drawProfileCard(doc, y, fields) {
  doc.setFillColor(...COLORS.surface);
  doc.setDrawColor(226, 232, 240);
  doc.roundedRect(14, y, 182, 38, 3, 3, 'FD');

  const col1 = 18;
  const col2 = 105;
  let row = y + 10;
  fields.forEach((item, index) => {
    const x = index % 2 === 0 ? col1 : col2;
    if (index % 2 === 0 && index > 0) row += 12;
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(7);
    doc.setTextColor(...COLORS.muted);
    doc.text(item.label.toUpperCase(), x, row);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(...COLORS.slate);
    doc.text(item.value || 'N/A', x, row + 5, { maxWidth: 82 });
  });

  return y + 46;
}

function drawScoreBadge(doc, y, score) {
  const color = scoreColor(score);
  doc.setFillColor(...color);
  doc.circle(32, y + 14, 14, 'F');
  doc.setTextColor(...COLORS.white);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text(String(score), 32, y + 17, { align: 'center' });

  doc.setTextColor(...COLORS.slate);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.text('ATS Match Score', 52, y + 10);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(...COLORS.muted);
  const hint = score >= 75
    ? 'Strong alignment with your target role.'
    : score >= 50
    ? 'Solid foundation with room to improve.'
    : 'Focus on closing skill gaps and resume clarity.';
  doc.text(hint, 52, y + 17, { maxWidth: 140 });
  doc.text('Score out of 100', 52, y + 24);

  return y + 36;
}

function ensureSpace(doc, y, needed = 40) {
  if (y + needed > 275) {
    doc.addPage();
    drawHeaderBanner(doc);
    return 52;
  }
  return y;
}

export function generateCareerReportPdf({
  candidateName,
  candidateEmail,
  candidatePhone,
  candidateCollege,
  detectedDomain,
  role,
  recommendedRoles,
  atsScore,
  matched,
  missing,
  careerSuggestions,
  roadmap,
  customRoadmap,
  jobsByRole,
}) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  drawHeaderBanner(doc);

  let y = 52;

  y = drawSectionTitle(doc, y, 'Candidate Profile', 'Details extracted from your uploaded resume');
  y = drawProfileCard(doc, y, [
    { label: 'Name', value: candidateName },
    { label: 'Email', value: candidateEmail },
    { label: 'Phone', value: candidatePhone },
    { label: 'College', value: candidateCollege },
  ]);

  y = ensureSpace(doc, y, 45);
  y = drawSectionTitle(doc, y, 'Analysis Summary');
  y = drawScoreBadge(doc, y, atsScore ?? 0);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(...COLORS.slate);
  const summaryLines = [
    `Domain: ${detectedDomain || 'Not specified'}`,
    `Target Role: ${role || 'N/A'}`,
    `Recommended Roles: ${(recommendedRoles || []).join(' · ') || 'N/A'}`,
  ];
  summaryLines.forEach((line) => {
    y = ensureSpace(doc, y, 8);
    doc.text(line, 14, y);
    y += 6;
  });
  y += 4;

  y = ensureSpace(doc, y, 30);
  y = drawSectionTitle(doc, y, 'Skills Analysis');

  autoTable(doc, {
    startY: y,
    head: [['Matched Skills', 'Skill Gaps']],
    body: [[
      matched.length ? matched.join(', ') : 'None detected in resume.',
      missing.length ? missing.join(', ') : 'No major gaps identified.',
    ]],
    theme: 'grid',
    styles: {
      fontSize: 9,
      cellPadding: 4,
      textColor: COLORS.slate,
      lineColor: [226, 232, 240],
      lineWidth: 0.2,
    },
    headStyles: {
      fillColor: COLORS.bg,
      textColor: COLORS.white,
      fontStyle: 'bold',
    },
    columnStyles: {
      0: { cellWidth: 91 },
      1: { cellWidth: 91 },
    },
    margin: { left: 14, right: 14 },
  });

  y = (doc.lastAutoTable?.finalY || y) + 10;

  y = ensureSpace(doc, y, 35);
  y = drawSectionTitle(doc, y, 'Career Suggestions', 'Personalized guidance based on your resume');
  doc.setFillColor(245, 243, 255);
  doc.setDrawColor(...COLORS.purple);
  const suggestionText = careerSuggestions || 'No career suggestions available.';
  const suggestionLines = doc.splitTextToSize(suggestionText, 174);
  const boxHeight = Math.max(22, suggestionLines.length * 4.5 + 10);
  doc.roundedRect(14, y, 182, boxHeight, 2, 2, 'FD');
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(...COLORS.slate);
  doc.text(suggestionLines, 18, y + 8);
  y += boxHeight + 8;

  const roadmapRows = (roadmap.length ? roadmap : []).map((step) => [
    String(step.step ?? ''),
    String(step.title ?? ''),
    String(step.focus ?? step.project_idea ?? ''),
  ]);

  if (!roadmapRows.length && (customRoadmap || []).length) {
    customRoadmap.forEach((line, index) => {
      roadmapRows.push([String(index + 1), `Milestone ${index + 1}`, String(line)]);
    });
  }

  if (!roadmapRows.length) {
    roadmapRows.push(['1', 'Unavailable', 'Upload a resume with more detail for a tailored roadmap.']);
  }

  y = ensureSpace(doc, y, 40);
  y = drawSectionTitle(doc, y, 'Learning Roadmap', 'Step-by-step milestones for your target role');

  autoTable(doc, {
    startY: y,
    head: [['Step', 'Milestone', 'Action Focus']],
    body: roadmapRows,
    theme: 'striped',
    styles: {
      fontSize: 8.5,
      cellPadding: 3,
      textColor: COLORS.slate,
      lineColor: [226, 232, 240],
    },
    headStyles: {
      fillColor: COLORS.purple,
      textColor: COLORS.white,
      fontStyle: 'bold',
    },
    columnStyles: {
      0: { cellWidth: 14, halign: 'center' },
      1: { cellWidth: 48 },
      2: { cellWidth: 120 },
    },
    margin: { left: 14, right: 14 },
  });

  y = (doc.lastAutoTable?.finalY || y) + 10;

  const jobRows = [];
  Object.entries(jobsByRole || {}).forEach(([roleKey, roleJobs]) => {
    (roleJobs || []).forEach((job) => {
      const url = String(job.redirect_url || job.job_apply_link || '').trim();
      const hasLink = url && url !== '#';
      jobRows.push([
        roleKey,
        String(job.company_name || job.employer_name || 'Company'),
        String(job.job_title || 'Open Role'),
        String(job.location || 'India'),
        hasLink
          ? { content: 'Apply', link: url, styles: { textColor: COLORS.purple, fontStyle: 'bold', halign: 'center' } }
          : { content: 'N/A', styles: { textColor: COLORS.muted, halign: 'center' } },
      ]);
    });
  });

  y = ensureSpace(doc, y, 40);
  y = drawSectionTitle(doc, y, 'Live Job Openings (India)', 'Click Apply to open the job posting');

  autoTable(doc, {
    startY: y,
    head: [['Role', 'Company', 'Job Title', 'Location', 'Link']],
    body: jobRows.length ? jobRows : [['—', '—', 'No listings found', '—', '—']],
    theme: 'grid',
    styles: {
      fontSize: 8,
      cellPadding: 3,
      textColor: COLORS.slate,
      lineColor: [226, 232, 240],
      overflow: 'linebreak',
    },
    headStyles: {
      fillColor: COLORS.bg,
      textColor: COLORS.white,
      fontStyle: 'bold',
    },
    columnStyles: {
      0: { cellWidth: 32 },
      1: { cellWidth: 38 },
      2: { cellWidth: 52 },
      3: { cellWidth: 28 },
      4: { cellWidth: 18 },
    },
    margin: { left: 14, right: 14 },
    didDrawPage: (data) => {
      if (data.pageNumber > 1) {
        drawHeaderBanner(doc);
      }
    },
  });

  const pageCount = doc.getNumberOfPages();
  for (let page = 1; page <= pageCount; page += 1) {
    doc.setPage(page);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(...COLORS.muted);
    doc.text(
      `Resume Analyzer · Page ${page} of ${pageCount}`,
      105,
      290,
      { align: 'center' },
    );
  }

  doc.save('Resume-Analyzer-Report.pdf');
}
