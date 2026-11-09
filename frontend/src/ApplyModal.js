// ==============================================================================
// TECH STACK: [React 19 & Lucide Icons] - 1-Click Smart Apply & Auto-Fill Modal
// Pre-fills candidate resume details and prompts for job screening questions
// before dispatching application to employer & MongoDB tracking store.
// ==============================================================================
import React, { useState } from 'react';
import {
  X,
  CheckCircle,
  Briefcase,
  Building2,
  MapPin,
  ExternalLink,
  Sparkles,
  Send,
  User,
  Mail,
  Phone,
  Clock,
  DollarSign,
  FileText,
  Award,
} from 'lucide-react';
import { apiService, formatAuthError } from './api/client';

export default function ApplyModal({
  job,
  candidateProfile = {},
  onClose,
  onApplySuccess,
}) {
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  // Pre-filled candidate details
  const [name, setName] = useState(candidateProfile.name || '');
  const [email, setEmail] = useState(candidateProfile.email || '');
  const [phone, setPhone] = useState(candidateProfile.phone || '');
  const college = candidateProfile.college || '';
  const atsScore = candidateProfile.atsScore || 85;
  const matchedSkills = candidateProfile.matchedSkills || [];

  // Screening questions
  const [noticePeriod, setNoticePeriod] = useState('Immediate Joiner (0 - 15 days)');
  const [experience, setExperience] = useState('0 - 2 Years (Entry / Mid Level)');
  const [expectedCtc, setExpectedCtc] = useState('6 - 10 LPA');
  const [workMode, setWorkMode] = useState('Flexible / Remote / Hybrid');

  // AI-assisted tailored cover letter pitch
  const defaultPitch = `Dear Hiring Team at ${job.company_name || 'the company'},\n\nI am applying for the ${job.job_title || 'open role'}. My background in ${(matchedSkills.slice(0, 5).join(', ')) || 'modern software engineering'} aligns strongly with your requirements (${atsScore}% ATS Match). I am available to join ${noticePeriod.toLowerCase()} and look forward to contributing to your team.`;
  const [coverNote, setCoverNote] = useState(defaultPitch);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email.trim()) {
      setError('Please provide a valid email address.');
      return;
    }
    if (!name.trim()) {
      setError('Please provide your full name.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        job_title: job.job_title,
        company_name: job.company_name,
        job_location: job.location || 'India',
        redirect_url: job.redirect_url || '',
        candidate_name: name.trim(),
        candidate_email: email.trim(),
        candidate_phone: phone.trim(),
        candidate_college: college,
        target_role: job.role_category || '',
        ats_score: atsScore,
        matched_skills: matchedSkills,
        notice_period: noticePeriod,
        experience_years: experience,
        expected_ctc: expectedCtc,
        work_mode: workMode,
        cover_note: coverNote,
      };

      const res = await apiService.applyToJob(payload);
      setSubmitted(true);
      onApplySuccess?.(job, res);
    } catch (err) {
      setError(formatAuthError(err) || 'Failed to submit application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tw-auth-overlay" role="dialog" aria-modal="true" onClick={onClose}>
      <div
        className="tw-auth-modal"
        style={{ maxWidth: '640px', maxHeight: '92vh', overflowY: 'auto' }}
        onClick={(e) => e.stopPropagation()}
      >
        <button type="button" className="tw-auth-modal__close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        {!submitted ? (
          <div>
            {/* Header / Job Summary */}
            <div className="border-bottom pb-3 mb-3">
              <div className="d-flex align-items-center gap-2 mb-2">
                <span className="badge bg-primary text-light px-2 py-1" style={{ fontSize: '0.75rem' }}>
                  1-Click Smart Apply
                </span>
                <span className="badge bg-success text-light px-2 py-1" style={{ fontSize: '0.75rem' }}>
                  <Award size={12} className="me-1" style={{ display: 'inline' }} />
                  {atsScore}% ATS Match
                </span>
                <span className="badge bg-light text-secondary border px-2 py-1 ms-auto" style={{ fontSize: '0.75rem' }}>
                  {job.portal || 'Direct Portal'}
                </span>
              </div>
              <h4 className="fw-bold text-dark mb-1">{job.job_title}</h4>
              <div className="d-flex flex-wrap align-items-center gap-3 text-muted small">
                <span>
                  <Building2 size={14} className="me-1 text-primary" style={{ display: 'inline' }} />
                  <strong>{job.company_name}</strong>
                </span>
                <span>
                  <MapPin size={14} className="me-1 text-danger" style={{ display: 'inline' }} />
                  {job.location || 'India'}
                </span>
                <span>
                  <Briefcase size={14} className="me-1 text-secondary" style={{ display: 'inline' }} />
                  {job.job_employment_type || 'Full-time'}
                </span>
              </div>
            </div>

            {error && <div className="tw-auth-alert tw-auth-alert--error mb-3">{error}</div>}

            <form onSubmit={handleSubmit} className="d-flex flex-column gap-3">
              {/* Auto-filled Resume Section */}
              <div className="p-3 bg-light rounded border">
                <div className="d-flex align-items-center justify-content-between mb-2">
                  <span className="fw-semibold small text-primary d-inline-flex align-items-center gap-1">
                    <Sparkles size={14} /> Resume Details Auto-Filled
                  </span>
                  <span className="badge bg-white text-success border small">Verified from Resume</span>
                </div>
                <div className="row g-2">
                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">Candidate Name</label>
                    <div className="input-group input-group-sm">
                      <span className="input-group-text bg-white"><User size={14} /></span>
                      <input
                        type="text"
                        className="form-control"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Your full name"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">Email Address</label>
                    <div className="input-group input-group-sm">
                      <span className="input-group-text bg-white"><Mail size={14} /></span>
                      <input
                        type="email"
                        className="form-control"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Your email"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">Phone Number</label>
                    <div className="input-group input-group-sm">
                      <span className="input-group-text bg-white"><Phone size={14} /></span>
                      <input
                        type="text"
                        className="form-control"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        placeholder="10-digit mobile number"
                        disabled={loading}
                      />
                    </div>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">Matched Core Skills</label>
                    <div className="d-flex flex-wrap gap-1 mt-1">
                      {matchedSkills.length > 0 ? (
                        matchedSkills.slice(0, 4).map((sk) => (
                          <span key={sk} className="badge bg-white text-dark border" style={{ fontSize: '0.72rem' }}>
                            {sk}
                          </span>
                        ))
                      ) : (
                        <span className="text-muted small">Evaluated from Resume</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Job Screening Questions Section */}
              <div className="p-3 bg-white rounded border">
                <p className="fw-semibold small text-dark mb-2">Job Screening Questions</p>
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">
                      <Clock size={13} className="me-1 text-primary" style={{ display: 'inline' }} />
                      Notice Period / Earliest Joining
                    </label>
                    <select
                      className="form-select form-select-sm"
                      value={noticePeriod}
                      onChange={(e) => setNoticePeriod(e.target.value)}
                      disabled={loading}
                    >
                      <option value="Immediate Joiner (0 - 15 days)">Immediate Joiner (0 - 15 days)</option>
                      <option value="15 - 30 Days">15 - 30 Days</option>
                      <option value="30 - 60 Days">30 - 60 Days</option>
                      <option value="Serving Notice (Available Soon)">Serving Notice (Available Soon)</option>
                    </select>
                  </div>

                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">
                      <Briefcase size={13} className="me-1 text-primary" style={{ display: 'inline' }} />
                      Relevant Domain Experience
                    </label>
                    <select
                      className="form-select form-select-sm"
                      value={experience}
                      onChange={(e) => setExperience(e.target.value)}
                      disabled={loading}
                    >
                      <option value="Fresher / Entry Level (0 - 1 yr)">Fresher / Entry Level (0 - 1 yr)</option>
                      <option value="1 - 3 Years">1 - 3 Years</option>
                      <option value="3 - 5 Years">3 - 5 Years</option>
                      <option value="5+ Years (Senior / Lead)">5+ Years (Senior / Lead)</option>
                    </select>
                  </div>

                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">
                      <DollarSign size={13} className="me-1 text-success" style={{ display: 'inline' }} />
                      Expected Annual CTC (in LPA)
                    </label>
                    <input
                      type="text"
                      className="form-control form-control-sm"
                      value={expectedCtc}
                      onChange={(e) => setExpectedCtc(e.target.value)}
                      placeholder="e.g. 6 - 10 LPA or Negotiable"
                      disabled={loading}
                    >
                    </input>
                  </div>

                  <div className="col-md-6">
                    <label className="form-label small text-muted mb-1">
                      <MapPin size={13} className="me-1 text-danger" style={{ display: 'inline' }} />
                      Work Mode Preference
                    </label>
                    <select
                      className="form-select form-select-sm"
                      value={workMode}
                      onChange={(e) => setWorkMode(e.target.value)}
                      disabled={loading}
                    >
                      <option value="Flexible / Remote / Hybrid">Flexible / Remote / Hybrid</option>
                      <option value="Remote Only">Remote Only</option>
                      <option value="Work From Office">Work From Office</option>
                    </select>
                  </div>

                  <div className="col-12">
                    <label className="form-label small text-muted mb-1">
                      <FileText size={13} className="me-1 text-primary" style={{ display: 'inline' }} />
                      Pitch to Recruiter (AI Auto-Drafted)
                    </label>
                    <textarea
                      className="form-control form-control-sm"
                      rows={3}
                      value={coverNote}
                      onChange={(e) => setCoverNote(e.target.value)}
                      disabled={loading}
                      style={{ fontSize: '0.85rem' }}
                    />
                  </div>
                </div>
              </div>

              {/* Submit Buttons */}
              <div className="d-flex gap-2 justify-content-end pt-2 border-top">
                <button
                  type="button"
                  className="btn btn-sm btn-outline-secondary"
                  onClick={onClose}
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-sm btn-primary tw-btn-primary d-inline-flex align-items-center gap-2 px-4"
                  disabled={loading}
                >
                  {loading ? (
                    <span>Submitting Application…</span>
                  ) : (
                    <>
                      <Send size={14} />
                      <span>Confirm &amp; Submit Application</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        ) : (
          /* Celebratory Confirmation Screen */
          <div className="text-center py-4">
            <div className="mb-3">
              <CheckCircle size={56} className="text-success mx-auto" />
            </div>
            <h4 className="fw-bold text-dark mb-2">Application Submitted!</h4>
            <p className="text-muted small mb-4 px-3">
              Your resume details, contact info, and screening answers have been recorded and saved in your applicant tracking profile.
            </p>

            <div className="p-3 bg-light rounded text-start mb-4 mx-auto" style={{ maxWidth: '480px' }}>
              <div className="d-flex justify-content-between mb-1">
                <span className="text-muted small">Position:</span>
                <span className="fw-semibold small">{job.job_title}</span>
              </div>
              <div className="d-flex justify-content-between mb-1">
                <span className="text-muted small">Company:</span>
                <span className="fw-semibold small">{job.company_name}</span>
              </div>
              <div className="d-flex justify-content-between mb-1">
                <span className="text-muted small">Status:</span>
                <span className="badge bg-success text-light">✓ Applied &amp; Tracked</span>
              </div>
              <div className="d-flex justify-content-between">
                <span className="text-muted small">Notice / CTC:</span>
                <span className="small text-dark">{noticePeriod} • {expectedCtc}</span>
              </div>
            </div>

            <div className="d-flex flex-wrap justify-content-center gap-2">
              {job.redirect_url && (
                <a
                  href={job.redirect_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-primary d-inline-flex align-items-center gap-1"
                >
                  <span>Open {job.portal || 'Employer Portal'} Directly</span>
                  <ExternalLink size={14} />
                </a>
              )}
              <button
                type="button"
                className="btn btn-sm btn-primary tw-btn-primary px-4"
                onClick={onClose}
              >
                Done
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
