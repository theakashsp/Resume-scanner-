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
import TechBackground from './TechBackground';
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

function BrandName({ variant = 'hero' }) {
  return (
    <div className={`ra-brand ra-brand--${variant}`}>
      <span className="ra-brand__resume">Resume</span>
      <span className="ra-brand__analyzer hx-gradient-text">Analyzer</span>
    </div>
  );
}

function Header({ scrolled }) {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header className={`hx-header hx-glass ${scrolled ? 'hx-header--scrolled' : ''}`}>
      <div className="hx-header__inner">
        <div className="hx-header__brand">
          <div className="hx-header__logo">RA</div>
          <BrandName variant="header" />
        </div>
        <nav className="hx-header__nav">
          <a href="#features" onClick={(e) => { e.preventDefault(); scrollTo('features'); }}>Features</a>
          <a href="#upload" onClick={(e) => { e.preventDefault(); scrollTo('upload'); }}>Upload</a>
          <a href="#process" onClick={(e) => { e.preventDefault(); scrollTo('process'); }}>Process</a>
          <a href="#dashboard" onClick={(e) => { e.preventDefault(); scrollTo('dashboard'); }}>Results</a>
        </nav>
        <button type="button" className="hx-header__cta" onClick={() => scrollTo('upload')}>
          Get Started
        </button>
      </div>
    </header>
  );
}

function StatsBar({ stats }) {
  const analyses = useCountUp(stats?.total_analyses ?? 0);
  const domains = useCountUp(stats?.domains_supported ?? 8);
  const roles = useCountUp(stats?.job_roles_per_scan ?? 5);
  const jobsPerRole = stats?.jobs_per_role ?? 4;

  const items = [
    { value: analyses, label: 'Resumes Analyzed' },
    { value: domains, label: 'Domains Supported' },
    { value: roles, label: 'Roles Per Scan' },
    { value: jobsPerRole, label: 'Jobs Per Role' },
  ];

  return (
    <div className="hx-stats">
      {items.map((item) => (
        <article key={item.label} className="hx-stat hx-glass">
          <div className="hx-stat__value">{item.value}{item.label === 'Jobs Per Role' ? '' : '+'}</div>
          <div className="hx-stat__label">{item.label}</div>
        </article>
      ))}
    </div>
  );
}

function FeaturesGrid({ features }) {
  return (
    <section id="features">
      <h2 className="hx-section-title hx-gradient-text">Platform Features</h2>
      <p className="hx-section-sub">Professional-grade career intelligence powered by modern technology</p>
      <div className="hx-features">
        {(features || []).map((feat) => {
          const Icon = FEATURE_ICONS[feat.icon] || Zap;
          return (
            <article key={feat.id} className="hx-feature hx-glass">
              <div className="hx-feature__icon">
                <Icon size={22} strokeWidth={2} />
              </div>
              <h3>{feat.title}</h3>
              <p>{feat.description}</p>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function ProcessTimeline({ step }) {
  const steps = [
    { id: 1, label: 'Upload Resume', icon: Upload },
    { id: 2, label: 'Deep Scan', icon: FileSearch },
    { id: 3, label: 'Results & Report', icon: FileText },
  ];
  return (
    <section className="hx-timeline hx-glass" id="process">
      <h2 className="hx-section-title">How It Works</h2>
      <p className="hx-section-sub">Three steps to your career intelligence dashboard</p>
      <div className="hx-timeline__track">
        {steps.map((s, index) => {
          const Icon = s.icon;
          const status = step > s.id ? 'done' : step === s.id ? 'active' : 'pending';
          return (
            <div key={s.id} className={`hx-timeline__step hx-timeline__step--${status}`}>
              <div className="hx-timeline__node">
                {status === 'done' ? <CheckCircle2 size={22} /> : <Icon size={22} />}
              </div>
              <span className="hx-timeline__label">{s.label}</span>
              {index < steps.length - 1 && <div className="hx-timeline__connector" />}
            </div>
          );
        })}
      </div>
    </section>
  );
}

function HeroUpload({ file, setFile, loading, error, onAnalyze }) {
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
    <div className="hx-upload hx-glass" id="upload">
      <div
        {...getRootProps()}
        className={`hx-dropzone ${isDragActive ? 'hx-dropzone--active' : ''} ${file ? 'hx-dropzone--ready' : ''} ${loading ? 'hx-dropzone--disabled' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="hx-dropzone__icon">
          <Upload size={32} strokeWidth={1.75} />
        </div>
        {file ? (
          <>
            <p className="hx-dropzone__title">{file.name}</p>
            <p className="hx-dropzone__meta">{(file.size / 1024).toFixed(1)} KB · ready for analysis</p>
          </>
        ) : (
          <>
            <p className="hx-dropzone__title">
              {isDragActive ? 'Release to upload your PDF' : 'Drag & drop your resume'}
            </p>
            <p className="hx-dropzone__meta">PDF only · click to browse</p>
          </>
        )}
      </div>

      <button
        type="button"
        className="hx-btn hx-btn--primary"
        onClick={onAnalyze}
        disabled={loading || !file}
      >
        {loading ? (
          <>
            <Loader2 className="hx-btn__spin" size={18} />
            Analyzing Resume
          </>
        ) : (
          'Launch Analysis'
        )}
      </button>

      {error && (
        <div className="hx-alert" role="alert">
          {error}
        </div>
      )}
    </div>
  );
}

function AtsScoreRing({ score }) {
  const radius = 58;
  const circ = 2 * Math.PI * radius;
  const offset = circ - (score / 100) * circ;
  const color = score >= 75 ? '#34d399' : score >= 50 ? '#fbbf24' : '#f87171';

  return (
    <div className="hx-score">
      <svg viewBox="0 0 140 140" className="hx-score__svg">
        <circle cx="70" cy="70" r={radius} className="hx-score__track" />
        <circle
          cx="70"
          cy="70"
          r={radius}
          className="hx-score__fill"
          style={{ strokeDasharray: circ, strokeDashoffset: offset, stroke: color }}
        />
      </svg>
      <div className="hx-score__label">
        <span className="hx-score__value" style={{ color }}>{score}</span>
        <span className="hx-score__caption">ATS Score</span>
      </div>
    </div>
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

  const loadingSteps = ['Parsing PDF', 'Extracting Skills', 'Matching Roles', 'Fetching Jobs'];

  return (
    <div className="hx-app">
      <TechBackground />
      <Header scrolled={scrolled} />

      <main className="hx-main">
        <section className="hx-hero">
          <div className="hx-hero__badge">
            <span className="hx-hero__badge-dot" />
            Career Intelligence Platform
          </div>
          <BrandName variant="hero" />
          <p className="hx-hero__subtitle">
            Upload your PDF resume for ATS scoring, precise skill extraction, and live India job matches.
            Personalized career roadmaps are delivered exclusively in your downloadable report.
          </p>
          <StatsBar stats={platformStats} />
          <FeaturesGrid features={features} />
          <HeroUpload
            file={file}
            setFile={setFile}
            loading={loading}
            error={error}
            onAnalyze={handleAnalyze}
          />
        </section>

        <ProcessTimeline step={timelineStep} />

        {loading && (
          <div className="hx-loading hx-glass" role="status" aria-live="polite">
            <Loader2 className="hx-loading__icon" size={36} />
            <p>Processing your resume…</p>
            <div className="hx-loading__steps">
              {loadingSteps.map((label, i) => (
                <span
                  key={label}
                  className={`hx-loading__step ${loadingStep >= i ? 'hx-loading__step--active' : ''}`}
                >
                  {loadingStep > i ? '✓ ' : ''}{label}
                </span>
              ))}
            </div>
          </div>
        )}

        {results && (
          <section className="hx-dashboard hx-glass" id="dashboard">
            <div className="hx-dashboard__header">
              <h2>Analysis Results</h2>
              <p>Your dashboard reflects the unique content extracted from your resume.</p>
            </div>

            <div className="hx-dashboard__meta">
              {[
                ['Name', candidateName],
                ['Email', candidateEmail],
                ['Phone', candidatePhone],
                ['College', candidateCollege],
                ['Domain', detectedDomain],
                ['Predicted Role', role || 'N/A'],
                ['Recommended Roles', recommendedRoles.length ? recommendedRoles.join(', ') : 'N/A'],
              ].map(([label, val]) => (
                <div key={label} className="hx-dashboard__meta-item">
                  <strong>{label}</strong>
                  {val}
                </div>
              ))}
            </div>

            <div className="hx-dashboard__grid">
              <div className="hx-card hx-glass hx-card--center">
                <AtsScoreRing score={results.ats_score ?? 0} />
                <p className="hx-card__hint">
                  {results.ats_score >= 75
                    ? 'Strong alignment for your target role.'
                    : results.ats_score >= 50
                    ? 'Solid foundation with room to close skill gaps.'
                    : 'Prioritize missing keywords and clearer resume structure.'}
                </p>
              </div>

              <div className="hx-card hx-glass">
                <h3>Matched Skills</h3>
                <ul className="hx-list">
                  {matched.length > 0 ? matched.map((s, i) => <li key={i}>{s}</li>) : (
                    <li className="hx-list__empty">No professional skills detected.</li>
                  )}
                </ul>

                <h3 className="hx-card__subtitle">Skill Gaps</h3>
                <div className="hx-chips">
                  {missing.length > 0 ? missing.map((s, i) => (
                    <span className="hx-chip" key={i}>{s}</span>
                  )) : (
                    <span className="hx-list__empty">No major gaps detected.</span>
                  )}
                </div>
              </div>
            </div>

            <div className="hx-dashboard__actions">
              <button type="button" className="hx-btn hx-btn--primary" onClick={generatePDFReport}>
                Download Career Report (PDF)
              </button>
              <p className="hx-dashboard__note">
                Career suggestions and milestone roadmaps are included in the PDF report only.
              </p>
            </div>

            <LiveJobOpenings
              recommendedRoles={recommendedRoles}
              jobsByRole={jobsByRole}
              jobsMessage={jobsMessage}
              jobsCount={jobsCount}
              loading={false}
            />
          </section>
        )}
      </main>

      <footer className="hx-footer hx-glass">
        <BrandName variant="footer" />
        <div className="hx-footer__links">
          <a href="#features">Features</a>
          <a href="#upload">Upload</a>
          <a href="#process">Process</a>
        </div>
        <span>© {new Date().getFullYear()} Resume Analyzer</span>
      </footer>
    </div>
  );
}

export default App;
