import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import {
  Upload,
  FileSearch,
  FileText,
  Target,
  Briefcase,
  CheckCircle2,
  Loader2,
  Layers,
  Globe,
  Shield,
  Route,
  Zap,
} from 'lucide-react';
import LiveJobOpenings from './LiveJobOpenings';
import { generateCareerReportPdf } from './pdfReport';
import './App.css';

const FEATURE_ICONS = {
  target: Target,
  layers: Layers,
  briefcase: Briefcase,
  route: Route,
  globe: Globe,
  shield: Shield,
};

function getApiOrigin() {
  const raw = process.env.REACT_APP_API_URL;
  if (raw != null && String(raw).trim() !== '') {
    return String(raw).trim().replace(/\/$/, '');
  }
  return 'http://127.0.0.1:8000';
}

function getAnalyzeUrl() {
  return `${getApiOrigin()}/analyze`;
}

function formatApiError(err) {
  const data = err.response?.data;
  if (data?.error) return data.error;
  if (data?.detail?.error) return data.detail.error;
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) {
    const joined = data.detail
      .map((x) => (typeof x === 'string' ? x : x?.msg))
      .filter(Boolean)
      .join('; ');
    if (joined) return joined;
  }
  if (data?.message) return data.message;
  if (err.response?.status) return `Request failed with status code ${err.response.status}`;
  return err.message || 'Analysis failed. Please try again.';
}

function useCountUp(target, duration = 1200) {
  const [value, setValue] = useState(0);
  const started = useRef(false);

  useEffect(() => {
    if (started.current || !target) return undefined;
    started.current = true;
    const start = performance.now();
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - (1 - progress) ** 3;
      setValue(Math.round(eased * target));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    return undefined;
  }, [target, duration]);

  return value;
}

function BrandName({ variant = 'header' }) {
  return (
    <div className={`ra-brand ra-brand--${variant}`}>
      <span className="ra-brand__resume">Resume</span>
      <span className="ra-brand__analyzer">Analyzer</span>
    </div>
  );
}

function Navbar({ scrolled }) {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <nav className={`tw-navbar ${scrolled ? 'tw-navbar--scrolled' : ''}`}>
      <div className="container tw-navbar__inner">
        <div className="tw-brand">
          <div className="tw-brand__icon">RA</div>
          <BrandName variant="header" />
        </div>
        <div className="tw-nav">
          <a href="#home" onClick={(e) => { e.preventDefault(); scrollTo('home'); }}>Home</a>
          <a href="#services" onClick={(e) => { e.preventDefault(); scrollTo('services'); }}>Services</a>
          <a href="#upload" onClick={(e) => { e.preventDefault(); scrollTo('upload'); }}>Analyze</a>
          <a href="#process" onClick={(e) => { e.preventDefault(); scrollTo('process'); }}>Process</a>
          <a href="#listings" onClick={(e) => { e.preventDefault(); scrollTo('listings'); }}>Listings</a>
        </div>
        <button type="button" className="btn btn-primary tw-btn-primary btn-sm" onClick={() => scrollTo('upload')}>
          Get Started
        </button>
      </div>
    </nav>
  );
}

function StatsBar({ stats }) {
  const analyses = useCountUp(stats?.total_analyses ?? 0);
  const domains = useCountUp(stats?.domains_supported ?? 8);
  const roles = useCountUp(stats?.job_roles_per_scan ?? 5);
  const jobsPerRole = stats?.jobs_per_role ?? 4;

  const items = [
    { value: analyses, label: 'Resumes Analyzed' },
    { value: domains, label: 'Career Domains' },
    { value: roles, label: 'Roles Per Scan' },
    { value: jobsPerRole, label: 'Listings Per Role' },
  ];

  return (
    <div className="tw-stats">
      {items.map((item) => (
        <article key={item.label} className="tw-stat">
          <div className="tw-stat__value">{item.value}{item.label === 'Listings Per Role' ? '' : '+'}</div>
          <div className="tw-stat__label">{item.label}</div>
        </article>
      ))}
    </div>
  );
}

function ServicesGrid({ features }) {
  return (
    <section id="services" className="tw-section tw-section--alt">
      <div className="container">
        <div className="tw-section-head text-center">
          <span className="tw-section-label">Our Services</span>
          <h2 className="tw-section-title">Professional Career Solutions</h2>
          <p className="tw-section-sub">
            Complete talent intelligence services — like a premium real estate agency, but for your career path
          </p>
        </div>
        <div className="row g-4">
          {(features || []).map((feat) => {
            const Icon = FEATURE_ICONS[feat.icon] || Zap;
            return (
              <div key={feat.id} className="col-md-6 col-lg-4">
                <article className="tw-service-card">
                  <div className="tw-service-card__icon">
                    <Icon size={24} strokeWidth={2} />
                  </div>
                  <h3>{feat.title}</h3>
                  <p>{feat.description}</p>
                </article>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function ProcessSteps({ step }) {
  const steps = [
    { id: 1, label: 'Upload Resume', icon: Upload },
    { id: 2, label: 'AI Deep Scan', icon: FileSearch },
    { id: 3, label: 'Career Report', icon: FileText },
  ];
  return (
    <section className="tw-section" id="process">
      <div className="container">
        <div className="tw-section-head text-center">
          <span className="tw-section-label">How It Works</span>
          <h2 className="tw-section-title">Your Career Journey in 3 Steps</h2>
        </div>
        <div className="tw-process">
          {steps.map((s) => {
            const Icon = s.icon;
            const status = step > s.id ? 'done' : step === s.id ? 'active' : 'pending';
            return (
              <div key={s.id} className={`tw-process__step tw-process__step--${status}`}>
                <div className="tw-process__node">
                  {status === 'done' ? <CheckCircle2 size={24} /> : <Icon size={24} />}
                </div>
                <span className="tw-process__label">{s.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function UploadSection({ file, setFile, loading, error, onAnalyze }) {
  const onDrop = useCallback((accepted) => {
    if (accepted?.[0]) setFile(accepted[0]);
  }, [setFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    multiple: false,
    disabled: loading,
  });

  return (
    <section className="tw-section" id="upload">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <div className="tw-section-head text-center mb-4">
              <span className="tw-section-label">Resume Analyzer</span>
              <h2 className="tw-section-title">Upload Your Resume for Analysis</h2>
              <p className="tw-section-sub">PDF format only — get ATS score, skills, gaps, and live job listings</p>
            </div>
            <div
              {...getRootProps()}
              className={`tw-upload-box ${isDragActive ? 'tw-upload-box--active' : ''} ${file ? 'tw-upload-box--ready' : ''} ${loading ? 'tw-upload-box--disabled' : ''}`}
            >
              <input {...getInputProps()} />
              <div className="tw-upload-box__icon">
                <Upload size={32} strokeWidth={1.75} />
              </div>
              {file ? (
                <>
                  <p className="tw-upload-box__title">{file.name}</p>
                  <p className="tw-upload-box__meta">{(file.size / 1024).toFixed(1)} KB · ready for analysis</p>
                </>
              ) : (
                <>
                  <p className="tw-upload-box__title">
                    {isDragActive ? 'Release to upload' : 'Drag & drop your resume PDF here'}
                  </p>
                  <p className="tw-upload-box__meta">or click to browse files</p>
                </>
              )}
            </div>
            <button
              type="button"
              className="btn btn-primary tw-btn-primary w-100"
              onClick={onAnalyze}
              disabled={loading || !file}
            >
              {loading ? (
                <>
                  <Loader2 className="tw-loading__icon d-inline-block me-2" size={18} style={{ animation: 'tw-spin 0.9s linear infinite' }} />
                  Analyzing Resume…
                </>
              ) : (
                'Launch Career Analysis'
              )}
            </button>
            {error && <div className="tw-alert" role="alert">{error}</div>}
          </div>
        </div>
      </div>
    </section>
  );
}

function AtsScoreRing({ score }) {
  const radius = 58;
  const circ = 2 * Math.PI * radius;
  const offset = circ - (score / 100) * circ;
  const color = score >= 75 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444';

  return (
    <div className="tw-score">
      <svg viewBox="0 0 140 140" className="tw-score__svg">
        <circle cx="70" cy="70" r={radius} className="tw-score__track" />
        <circle
          cx="70"
          cy="70"
          r={radius}
          className="tw-score__fill"
          style={{ strokeDasharray: circ, strokeDashoffset: offset, stroke: color }}
        />
      </svg>
      <div className="tw-score__label">
        <span className="tw-score__value" style={{ color }}>{score}</span>
        <span className="tw-score__caption">ATS Score</span>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <footer className="tw-footer">
      <div className="container">
        <div className="tw-footer__bottom">
          © {new Date().getFullYear()} Resume Analyzer · Career Intelligence Platform
        </div>
      </div>
    </footer>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [platformStats, setPlatformStats] = useState(null);
  const [features, setFeatures] = useState([]);
  const [scrolled, setScrolled] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);

  const timelineStep = useMemo(() => {
    if (results) return 3;
    if (loading) return 2;
    if (file) return 2;
    return 1;
  }, [file, loading, results]);

  useEffect(() => {
    const api = getApiOrigin();
    axios.get(`${api}/api/platform-stats`).then((r) => setPlatformStats(r.data)).catch(() => {});
    axios.get(`${api}/api/features`).then((r) => setFeatures(r.data?.features || [])).catch(() => {});
  }, []);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (!loading) {
      setLoadingStep(0);
      return undefined;
    }
    const timers = [
      setTimeout(() => setLoadingStep(1), 800),
      setTimeout(() => setLoadingStep(2), 3000),
      setTimeout(() => setLoadingStep(3), 6000),
    ];
    return () => timers.forEach(clearTimeout);
  }, [loading]);

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('file', file, file.name);
      const response = await axios.post(getAnalyzeUrl(), formData, { timeout: 120000 });

      if (response.data?.error) {
        setError(response.data.error);
        return;
      }

      setResults(response.data);
      const api = getApiOrigin();
      axios.get(`${api}/api/platform-stats`).then((r) => setPlatformStats(r.data)).catch(() => {});
      setTimeout(() => {
        document.getElementById('dashboard')?.scrollIntoView({ behavior: 'smooth' });
      }, 300);
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const matched = results?.matched_skills ?? [];
  const missing = results?.missing_skills ?? [];
  const role = results?.predicted_role;
  const roadmap = results?.learning_roadmap ?? [];
  const careerSuggestions = results?.career_suggestions ?? results?.custom_suggestion ?? '';
  const meta = results?.candidate_metadata ?? {};
  const candidateName = meta.candidate_name || results?.candidate_name || 'Not found';
  const candidateEmail = meta.candidate_email || results?.candidate_email || 'Not found';
  const candidatePhone = meta.candidate_phone || results?.candidate_phone || 'Not found';
  const candidateCollege = meta.candidate_college || results?.candidate_college || 'Not found';
  const detectedDomain = results?.detected_domain || 'Not specified';
  const recommendedRoles = results?.recommended_roles ?? [];
  const jobsByRole = results?.jobs_by_role ?? {};
  const jobsMessage = results?.jobs_message ?? null;
  const jobsCount = results?.jobs_count ?? 0;

  const generatePDFReport = () => {
    if (!results) return;
    generateCareerReportPdf({
      candidateName,
      candidateEmail,
      candidatePhone,
      candidateCollege,
      detectedDomain,
      role,
      recommendedRoles,
      atsScore: results.ats_score ?? 0,
      matched,
      missing,
      careerSuggestions,
      roadmap,
      customRoadmap: results?.custom_roadmap ?? [],
      jobsByRole,
    });
  };

  const loadingSteps = ['Parsing PDF', 'Extracting Skills', 'Matching Roles', 'Fetching Listings'];

  return (
    <div className="tw-app">
      <Navbar scrolled={scrolled} />

      <section className="tw-hero" id="home">
        <div className="container">
          <p className="tw-hero__breadcrumb">
            Home <span>/</span> Career Agency <span>/</span> Resume Analyzer
          </p>
          <BrandName variant="hero" />
          <h1 className="tw-hero__title">
            Find Your <em>Perfect Career Match</em>
          </h1>
          <p className="tw-hero__sub">
            Resume Analyzer delivers premium resume analysis, ATS scoring, skill mapping,
            and live India job listings — tailored exclusively from your uploaded resume.
          </p>
          <div className="tw-hero__actions">
            <button type="button" className="btn btn-primary tw-btn-primary" onClick={() => document.getElementById('upload')?.scrollIntoView({ behavior: 'smooth' })}>
              Analyze My Resume
            </button>
            <button type="button" className="btn tw-btn-outline" onClick={() => document.getElementById('services')?.scrollIntoView({ behavior: 'smooth' })}>
              Explore Services
            </button>
          </div>
        </div>
      </section>

      <div className="container">
        <div className="tw-hero-search">
          <StatsBar stats={platformStats} />
        </div>
      </div>

      <ServicesGrid features={features} />
      <UploadSection
        file={file}
        setFile={setFile}
        loading={loading}
        error={error}
        onAnalyze={handleAnalyze}
      />
      <ProcessSteps step={timelineStep} />

      {loading && (
        <div className="container">
          <div className="tw-loading" role="status" aria-live="polite">
            <Loader2 className="tw-loading__icon" size={36} />
            <p>Processing your resume…</p>
            <div className="tw-loading__steps">
              {loadingSteps.map((label, i) => (
                <span key={label} className={`tw-loading__step ${loadingStep >= i ? 'tw-loading__step--active' : ''}`}>
                  {loadingStep > i ? '✓ ' : ''}{label}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {results && (
        <section className="tw-section tw-section--alt" id="dashboard">
          <div className="container">
            <div className="tw-section-head text-center mb-4">
              <span className="tw-section-label">Analysis Report</span>
              <h2 className="tw-section-title">Your Career Profile</h2>
              <p className="tw-section-sub">Insights derived exclusively from your uploaded resume</p>
            </div>

            <div className="tw-dashboard">
              <div className="tw-dashboard__meta">
                {[
                  ['Candidate Name', candidateName],
                  ['Email', candidateEmail],
                  ['Phone', candidatePhone],
                  ['College', candidateCollege],
                  ['Domain', detectedDomain],
                  ['Target Role', role || 'N/A'],
                  ['Recommended Roles', recommendedRoles.length ? recommendedRoles.join(', ') : 'N/A'],
                ].map(([label, val]) => (
                  <div key={label} className="tw-dashboard__meta-item">
                    <strong>{label}</strong>
                    {val}
                  </div>
                ))}
              </div>

              <div className="tw-dashboard__grid">
                <div className="tw-card tw-card--center">
                  <AtsScoreRing score={results.ats_score ?? 0} />
                  <p className="tw-card__hint">
                    {results.ats_score >= 75
                      ? 'Strong alignment for your target role.'
                      : results.ats_score >= 50
                      ? 'Solid foundation with room to close skill gaps.'
                      : 'Prioritize missing keywords and clearer resume structure.'}
                  </p>
                </div>

                <div className="tw-card">
                  <h3>Matched Skills</h3>
                  <ul className="tw-list">
                    {matched.length > 0 ? matched.map((s, i) => <li key={i}>{s}</li>) : (
                      <li className="tw-list__empty">No professional skills detected.</li>
                    )}
                  </ul>
                  <h3 className="tw-card__subtitle">Skill Gaps</h3>
                  <div className="tw-chips">
                    {missing.length > 0 ? missing.map((s, i) => (
                      <span className="tw-chip" key={i}>{s}</span>
                    )) : (
                      <span className="tw-list__empty">No major gaps detected.</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="text-center mb-4">
                <button type="button" className="btn btn-primary tw-btn-primary" onClick={generatePDFReport}>
                  Download Career Report (PDF)
                </button>
                <p className="text-muted mt-2 small">
                  Career suggestions and milestone roadmaps are included in the PDF report only.
                </p>
              </div>

              <div id="listings">
                <LiveJobOpenings
                  recommendedRoles={recommendedRoles}
                  jobsByRole={jobsByRole}
                  jobsMessage={jobsMessage}
                  jobsCount={jobsCount}
                  loading={false}
                />
              </div>
            </div>
          </div>
        </section>
      )}

      <Footer />
    </div>
  );
}

export default App;
