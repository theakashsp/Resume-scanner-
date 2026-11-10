// ==============================================================================
// TECH STACK: [React 19 & Lucide Icons] - Applied Jobs & Status Tracker Modal
// Displays all submitted applications, confirmation email dispatch status,
// and incoming recruiter replies with live simulated response testing.
// ==============================================================================
import React, { useState, useEffect, useMemo } from 'react';
import {
  X,
  Briefcase,
  Building2,
  MapPin,
  Clock,
  Mail,
  CheckCircle,
  MessageSquare,
  Sparkles,
  Award,
  ExternalLink,
  Send,
  RefreshCw,
  Calendar,
  AlertCircle,
  CheckCheck,
} from 'lucide-react';
import { apiService, formatAuthError } from './api/client';

export default function ApplicationsModal({
  isOpen,
  onClose,
  candidateEmail = '',
  onApplicationUpdated,
}) {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [replyingAppId, setReplyingAppId] = useState(null);
  const [replyMessage, setReplyMessage] = useState('');
  const [replyRecruiter, setReplyRecruiter] = useState('Talent Acquisition Lead');
  const [replyStatus, setReplyStatus] = useState('Interview Scheduled');
  const [submittingReply, setSubmittingReply] = useState(false);

  const fetchApplications = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await apiService.getApplications(candidateEmail);
      if (res?.applications && Array.isArray(res.applications)) {
        setApplications(res.applications);
      } else {
        setApplications([]);
      }
    } catch (err) {
      setError(formatAuthError(err) || 'Failed to load applied jobs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchApplications();
    }
  }, [isOpen, candidateEmail]);

  const handleSimulateReply = async (appId) => {
    if (!replyMessage.trim()) return;
    setSubmittingReply(true);
    try {
      await apiService.replyToApplication(appId, {
        reply_message: replyMessage.trim(),
        new_status: replyStatus,
        interviewer_name: replyRecruiter.trim() || 'Hiring Manager',
      });
      setReplyingAppId(null);
      setReplyMessage('');
      await fetchApplications();
      onApplicationUpdated?.();
    } catch (err) {
      alert(formatAuthError(err) || 'Failed to record recruiter reply.');
    } finally {
      setSubmittingReply(false);
    }
  };

  const openReplyBox = (app, defaultMsg = '', defaultSt = 'Interview Scheduled') => {
    setReplyingAppId(app.id || app.job_key);
    setReplyRecruiter(`${app.company_name} Talent Team`);
    setReplyStatus(defaultSt);
    setReplyMessage(
      defaultMsg ||
        `Hi ${app.candidate_name || 'Candidate'}, we reviewed your application for the ${app.job_title} role (${app.ats_score || 85}% ATS match). We are impressed by your background and would like to invite you for a virtual interview this week!`
    );
  };

  const filteredApps = useMemo(() => {
    if (filterStatus === 'ALL') return applications;
    return applications.filter((app) => {
      const st = (app.status || '').toLowerCase();
      if (filterStatus === 'REPLIED') {
        return st.includes('reply') || st.includes('replied') || (app.recruiter_replies && app.recruiter_replies.length > 0);
      }
      if (filterStatus === 'INTERVIEW') {
        return st.includes('interview');
      }
      if (filterStatus === 'CONFIRMED') {
        return st.includes('confirm') || st.includes('applied');
      }
      return true;
    });
  }, [applications, filterStatus]);

  if (!isOpen) return null;

  const countReplied = applications.filter(
    (a) => (a.status || '').toLowerCase().includes('replied') || (a.recruiter_replies && a.recruiter_replies.length > 0)
  ).length;

  const countInterviews = applications.filter(
    (a) => (a.status || '').toLowerCase().includes('interview')
  ).length;

  return (
    <div className="tw-auth-overlay" role="dialog" aria-modal="true" onClick={onClose}>
      <div
        className="tw-auth-modal"
        style={{
          maxWidth: '820px',
          width: '95%',
          maxHeight: '92vh',
          display: 'flex',
          flexDirection: 'column',
          padding: 0,
          overflow: 'hidden',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Top Header */}
        <div
          className="d-flex align-items-center justify-content-between p-3 border-bottom"
          style={{ background: 'linear-gradient(135deg, #0f172a, #1e293b)', color: '#fff' }}
        >
          <div className="d-flex align-items-center gap-2">
            <div
              className="d-flex align-items-center justify-content-center rounded-circle"
              style={{ width: '36px', height: '36px', background: 'rgba(59, 130, 246, 0.2)', border: '1px solid rgba(59, 130, 246, 0.4)' }}
            >
              <Briefcase size={18} className="text-info" />
            </div>
            <div>
              <h5 className="mb-0 fw-bold" style={{ fontSize: '1.1rem', letterSpacing: '-0.01em' }}>
                Applied Jobs Tracker
              </h5>
              <p className="mb-0 small text-white-50" style={{ fontSize: '0.78rem' }}>
                Track submitted applications, automated emails & recruiter replies
              </p>
            </div>
          </div>
          <div className="d-flex align-items-center gap-2">
            <button
              type="button"
              className="btn btn-sm btn-outline-light d-inline-flex align-items-center gap-1"
              onClick={fetchApplications}
              disabled={loading}
              title="Refresh status"
            >
              <RefreshCw size={13} className={loading ? 'fa-spin' : ''} />
              <span className="d-none d-sm-inline">Refresh</span>
            </button>
            <button
              type="button"
              className="tw-auth-modal__close text-white"
              style={{ position: 'static', background: 'transparent' }}
              onClick={onClose}
              aria-label="Close"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Status Counter Bar */}
        <div className="bg-light p-3 border-bottom">
          <div className="row g-2 text-center">
            <div className="col-3">
              <div
                className={`p-2 rounded border bg-white ${filterStatus === 'ALL' ? 'border-primary shadow-sm' : ''}`}
                style={{ cursor: 'pointer' }}
                onClick={() => setFilterStatus('ALL')}
              >
                <div className="fw-bold text-dark fs-5">{applications.length}</div>
                <div className="small text-muted" style={{ fontSize: '0.75rem' }}>Total Applied</div>
              </div>
            </div>
            <div className="col-3">
              <div
                className={`p-2 rounded border bg-white ${filterStatus === 'CONFIRMED' ? 'border-info shadow-sm' : ''}`}
                style={{ cursor: 'pointer' }}
                onClick={() => setFilterStatus('CONFIRMED')}
              >
                <div className="fw-bold text-info fs-5">{applications.length}</div>
                <div className="small text-muted" style={{ fontSize: '0.75rem' }}>Emails Dispatched</div>
              </div>
            </div>
            <div className="col-3">
              <div
                className={`p-2 rounded border bg-white ${filterStatus === 'REPLIED' ? 'border-warning shadow-sm' : ''}`}
                style={{ cursor: 'pointer' }}
                onClick={() => setFilterStatus('REPLIED')}
              >
                <div className="fw-bold text-warning fs-5">{countReplied}</div>
                <div className="small text-muted" style={{ fontSize: '0.75rem' }}>Recruiter Replies</div>
              </div>
            </div>
            <div className="col-3">
              <div
                className={`p-2 rounded border bg-white ${filterStatus === 'INTERVIEW' ? 'border-success shadow-sm' : ''}`}
                style={{ cursor: 'pointer' }}
                onClick={() => setFilterStatus('INTERVIEW')}
              >
                <div className="fw-bold text-success fs-5">{countInterviews}</div>
                <div className="small text-muted" style={{ fontSize: '0.75rem' }}>Interviews Set</div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-3" style={{ overflowY: 'auto', flex: 1, maxHeight: '60vh' }}>
          {error && (
            <div className="alert alert-danger py-2 px-3 small d-flex align-items-center gap-2 mb-3">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {loading && applications.length === 0 ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary spinner-border-sm mb-2" role="status" />
              <p className="text-muted small mb-0">Loading your applications &amp; recruiter statuses…</p>
            </div>
          ) : filteredApps.length === 0 ? (
            <div className="text-center py-5 border rounded bg-light">
              <Briefcase size={36} className="text-muted mb-2 opacity-50" />
              <h6 className="fw-semibold text-dark">No applications found in this view</h6>
              <p className="text-muted small mb-3">
                {applications.length === 0
                  ? "You haven't submitted any job applications yet. Click 'Apply with Resume' on any live job opening!"
                  : 'Try selecting a different filter above.'}
              </p>
              {filterStatus !== 'ALL' && (
                <button
                  type="button"
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => setFilterStatus('ALL')}
                >
                  Show All Applications
                </button>
              )}
            </div>
          ) : (
            <div className="d-flex flex-column gap-3">
              {filteredApps.map((app, idx) => {
                const appliedDate = app.created_at
                  ? new Date(app.created_at * 1000).toLocaleString('en-IN', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })
                  : 'Recently';

                const statusLower = (app.status || 'applied').toLowerCase();
                let statusBadge = (
                  <span className="badge bg-primary text-white d-inline-flex align-items-center gap-1">
                    <CheckCircle size={11} /> Applied
                  </span>
                );

                if (statusLower.includes('interview')) {
                  statusBadge = (
                    <span className="badge bg-success text-white d-inline-flex align-items-center gap-1 px-2 py-1">
                      <Calendar size={11} /> Interview Scheduled
                    </span>
                  );
                } else if (statusLower.includes('replied')) {
                  statusBadge = (
                    <span className="badge bg-warning text-dark d-inline-flex align-items-center gap-1 px-2 py-1">
                      <MessageSquare size={11} /> Recruiter Replied
                    </span>
                  );
                } else if (statusLower.includes('confirmation') || app.email_sent) {
                  statusBadge = (
                    <span className="badge bg-info text-white d-inline-flex align-items-center gap-1 px-2 py-1">
                      <Mail size={11} /> Confirmation Sent
                    </span>
                  );
                }

                const replies = app.recruiter_replies || [];
                const isReplyingThis = replyingAppId === (app.id || app.job_key);

                return (
                  <div
                    key={app.id || app.job_key || idx}
                    className="card border shadow-sm"
                    style={{ borderRadius: '10px', overflow: 'hidden' }}
                  >
                    <div className="card-body p-3">
                      {/* Top Header of Job Card */}
                      <div className="d-flex flex-wrap align-items-start justify-content-between gap-2 mb-2">
                        <div>
                          <div className="d-flex align-items-center gap-2 mb-1">
                            <span className="fw-bold text-dark fs-6">{app.job_title}</span>
                            {statusBadge}
                          </div>
                          <div className="d-flex flex-wrap align-items-center gap-3 text-muted small">
                            <span className="fw-medium text-primary">
                              <Building2 size={13} className="me-1" style={{ display: 'inline' }} />
                              {app.company_name}
                            </span>
                            <span>
                              <MapPin size={13} className="me-1 text-danger" style={{ display: 'inline' }} />
                              {app.job_location || 'India'}
                            </span>
                            <span>
                              <Clock size={13} className="me-1 text-secondary" style={{ display: 'inline' }} />
                              Applied {appliedDate}
                            </span>
                          </div>
                        </div>

                        {/* ATS Score Tag */}
                        <div className="text-end">
                          <span
                            className="badge bg-light text-dark border px-2 py-1 d-inline-flex align-items-center gap-1"
                            style={{ fontSize: '0.75rem' }}
                          >
                            <Award size={12} className="text-primary" />
                            {app.ats_score || 85}% ATS Match
                          </span>
                        </div>
                      </div>

                      {/* Candidate details & Email Confirmation Banner */}
                      <div
                        className="p-2 rounded mb-2 d-flex flex-wrap align-items-center justify-content-between gap-2"
                        style={{ background: '#f8fafc', border: '1px solid #e2e8f0', fontSize: '0.8rem' }}
                      >
                        <div className="d-flex align-items-center gap-1 text-success fw-medium">
                          <CheckCheck size={14} />
                          <span>
                            Confirmation email sent to <strong>{app.candidate_email}</strong>
                          </span>
                        </div>
                        <div className="text-muted small">
                          <span>Notice: <strong>{app.notice_period || 'Immediate'}</strong></span>
                          <span className="mx-1">•</span>
                          <span>CTC: <strong>{app.expected_ctc || 'Negotiable'}</strong></span>
                        </div>
                      </div>

                      {/* Recruiter Reply Messages Section */}
                      {replies.length > 0 && (
                        <div className="mt-2 mb-2 pt-2 border-top">
                          <div className="d-flex align-items-center gap-1 mb-2 text-warning fw-semibold small">
                            <MessageSquare size={14} />
                            <span>Recruiter Responses ({replies.length}):</span>
                          </div>
                          <div className="d-flex flex-column gap-2">
                            {replies.map((reply, rIdx) => {
                              const replyTime = reply.created_at
                                ? new Date(reply.created_at * 1000).toLocaleString('en-IN', {
                                    month: 'short',
                                    day: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit',
                                  })
                                : 'Just now';

                              return (
                                <div
                                  key={reply.id || rIdx}
                                  className="p-2 rounded"
                                  style={{
                                    background: '#fffbeb',
                                    border: '1px solid #fef3c7',
                                    borderLeft: '4px solid #f59e0b',
                                  }}
                                >
                                  <div className="d-flex justify-content-between align-items-center mb-1">
                                    <span className="fw-semibold text-dark small" style={{ fontSize: '0.82rem' }}>
                                      {reply.recruiter_name || 'Hiring Team'}
                                    </span>
                                    <span className="text-muted" style={{ fontSize: '0.72rem' }}>
                                      {replyTime}
                                    </span>
                                  </div>
                                  <p className="mb-0 text-dark small" style={{ whiteSpace: 'pre-line', fontSize: '0.85rem' }}>
                                    {reply.message}
                                  </p>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      {/* Interactive Recruiter Reply Simulator Form */}
                      {isReplyingThis ? (
                        <div className="mt-3 p-3 bg-light rounded border">
                          <div className="d-flex justify-content-between align-items-center mb-2">
                            <span className="fw-semibold small text-dark d-inline-flex align-items-center gap-1">
                              <Sparkles size={14} className="text-warning" />
                              Simulate Incoming Recruiter Response
                            </span>
                            <button
                              type="button"
                              className="btn btn-sm btn-link text-muted p-0 text-decoration-none"
                              onClick={() => setReplyingAppId(null)}
                            >
                              Cancel
                            </button>
                          </div>
                          <div className="mb-2">
                            <label className="form-label small text-muted mb-1">Update Status To:</label>
                            <select
                              className="form-select form-select-sm"
                              value={replyStatus}
                              onChange={(e) => setReplyStatus(e.target.value)}
                            >
                              <option value="Interview Scheduled">Interview Scheduled (Calendar Invite)</option>
                              <option value="Recruiter Replied">Recruiter Replied (Screening Discussion)</option>
                              <option value="Under Technical Review">Under Technical Review (Hiring Manager)</option>
                              <option value="Offer Extended">Offer Extended (Shortlisted)</option>
                            </select>
                          </div>
                          <div className="mb-2">
                            <label className="form-label small text-muted mb-1">Recruiter Message:</label>
                            <textarea
                              rows={3}
                              className="form-control form-control-sm"
                              value={replyMessage}
                              onChange={(e) => setReplyMessage(e.target.value)}
                              placeholder="Write recruiter message..."
                            />
                          </div>
                          <div className="d-flex justify-content-end gap-2">
                            <button
                              type="button"
                              className="btn btn-sm btn-secondary"
                              onClick={() => setReplyingAppId(null)}
                            >
                              Cancel
                            </button>
                            <button
                              type="button"
                              className="btn btn-sm btn-success d-inline-flex align-items-center gap-1"
                              onClick={() => handleSimulateReply(app.id || app.job_key)}
                              disabled={submittingReply || !replyMessage.trim()}
                            >
                              <Send size={12} />
                              <span>{submittingReply ? 'Sending…' : 'Record Recruiter Reply'}</span>
                            </button>
                          </div>
                        </div>
                      ) : (
                        /* Action Footer */
                        <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-2 pt-2 border-top">
                          <div className="d-flex align-items-center gap-1">
                            <button
                              type="button"
                              className="btn btn-xs btn-outline-warning d-inline-flex align-items-center gap-1"
                              style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
                              onClick={() => openReplyBox(app)}
                            >
                              <MessageSquare size={12} />
                              <span>Simulate Recruiter Reply</span>
                            </button>
                            <button
                              type="button"
                              className="btn btn-xs btn-outline-success d-inline-flex align-items-center gap-1"
                              style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
                              onClick={() =>
                                openReplyBox(
                                  app,
                                  `Congratulations ${app.candidate_name || 'Candidate'}! The team at ${app.company_name} was very impressed by your ATS match score (${app.ats_score || 85}%). We are pleased to confirm your Technical Interview round scheduled for tomorrow at 3:00 PM IST via Google Meet.`,
                                  'Interview Scheduled'
                                )
                              }
                            >
                              <Calendar size={12} />
                              <span>Schedule Interview</span>
                            </button>
                          </div>

                          {app.redirect_url && (
                            <a
                              href={app.redirect_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="btn btn-xs btn-outline-primary d-inline-flex align-items-center gap-1 ms-auto"
                              style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
                            >
                              <span>Employer Career Page</span>
                              <ExternalLink size={11} />
                            </a>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-3 bg-light border-top d-flex justify-content-between align-items-center">
          <span className="small text-muted">
            Live persistence via MongoDB Atlas with automatic candidate email dispatch
          </span>
          <button type="button" className="btn btn-sm btn-primary tw-btn-primary px-4" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

