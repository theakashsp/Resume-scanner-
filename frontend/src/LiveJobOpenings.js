// ==============================================================================
// TECH STACK: [React 19 & Lucide Icons] - Live Job Openings Interactive Dashboard
// Displays live opportunities aggregated from Jobvetta / JSearch / Adzuna APIs
// with 1-Click Smart Apply, resume auto-fill, and candidate screening dialog.
// ==============================================================================
import React, { useState, useMemo, useEffect } from 'react';
import {
  MapPin,
  Briefcase,
  Building2,
  ExternalLink,
  Search,
  Filter,
  Sparkles,
  CheckCircle,
  Send,
} from 'lucide-react';
import ApplyModal from './ApplyModal';
import { apiService } from './api/client';

function getCompanyBranding(name) {
  const lower = (name || '').toLowerCase();
  if (lower.includes('amazon') || lower.includes('aws')) {
    return {
      gradient: 'linear-gradient(135deg, #131921 0%, #232f3e 60%, #ff9900 100%)',
      logoBg: '#ff9900',
      logoColor: '#131921',
      abbr: 'a',
      cleanName: lower.includes('aws') ? 'Amazon Web Services (AWS)' : 'Amazon',
    };
  }
  if (lower.includes('zomato')) {
    return {
      gradient: 'linear-gradient(135deg, #b91c1c 0%, #e11d48 60%, #991b1b 100%)',
      logoBg: '#ffffff',
      logoColor: '#e11d48',
      abbr: 'Z',
      cleanName: 'Zomato',
    };
  }
  if (lower.includes('swiggy')) {
    return {
      gradient: 'linear-gradient(135deg, #ea580c 0%, #f97316 60%, #c2410c 100%)',
      logoBg: '#ffffff',
      logoColor: '#ea580c',
      abbr: 'S',
      cleanName: 'Swiggy',
    };
  }
  if (lower.includes('google')) {
    return {
      gradient: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #4285f4 100%)',
      logoBg: '#ffffff',
      logoColor: '#2563eb',
      abbr: 'G',
      cleanName: 'Google',
    };
  }
  if (lower.includes('microsoft')) {
    return {
      gradient: 'linear-gradient(135deg, #0078d4 0%, #005a9e 60%, #002050 100%)',
      logoBg: '#ffffff',
      logoColor: '#0078d4',
      abbr: 'MS',
      cleanName: 'Microsoft',
    };
  }
  if (lower.includes('flipkart')) {
    return {
      gradient: 'linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #f59e0b 100%)',
      logoBg: '#f59e0b',
      logoColor: '#1d4ed8',
      abbr: 'Fk',
      cleanName: 'Flipkart',
    };
  }
  if (lower.includes('cred')) {
    return {
      gradient: 'linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #334155 100%)',
      logoBg: '#ffffff',
      logoColor: '#0f172a',
      abbr: 'CR',
      cleanName: 'CRED',
    };
  }
  if (lower.includes('razorpay')) {
    return {
      gradient: 'linear-gradient(135deg, #0c2340 0%, #0284c7 60%, #00baf2 100%)',
      logoBg: '#00baf2',
      logoColor: '#0c2340',
      abbr: 'Rz',
      cleanName: 'Razorpay',
    };
  }
  if (lower.includes('phonepe')) {
    return {
      gradient: 'linear-gradient(135deg, #581c87 0%, #6d28d9 60%, #7c3aed 100%)',
      logoBg: '#ffffff',
      logoColor: '#581c87',
      abbr: 'Pe',
      cleanName: 'PhonePe',
    };
  }
  if (lower.includes('infosys')) {
    return {
      gradient: 'linear-gradient(135deg, #0284c7 0%, #0369a1 60%, #075985 100%)',
      logoBg: '#ffffff',
      logoColor: '#0284c7',
      abbr: 'Inf',
      cleanName: 'Infosys',
    };
  }
  if (lower.includes('tcs')) {
    return {
      gradient: 'linear-gradient(135deg, #1e293b 0%, #334155 60%, #0f172a 100%)',
      logoBg: '#3b82f6',
      logoColor: '#ffffff',
      abbr: 'TCS',
      cleanName: 'TCS',
    };
  }

  const clean = name.replace(/\b(careers|jobs|network|partners|india|limited|ltd|pvt)\b/gi, '').trim() || name;
  return {
    gradient: 'linear-gradient(135deg, #1e293b 0%, #2563eb 100%)',
    logoBg: '#ffffff',
    logoColor: '#1e293b',
    abbr: clean.slice(0, 2).toUpperCase(),
    cleanName: clean,
  };
}

function normalizeJob(job) {
  const role = job.role_category || 'Software Professional';
  const title = job.job_title || job.title || role;
  let rawCompany = job.company_name || job.employer_name || 'Hiring Company';
  const branding = getCompanyBranding(rawCompany);
  const company = branding.cleanName || rawCompany;
  const location = job.location || 'India';

  let url = String(job.redirect_url || job.job_apply_link || job.link || '').trim();
  if (!url || url === '#' || !url.startsWith('http')) {
    url = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(`${company} ${title}`)}&location=India`;
  }

  return {
    role_category: role,
    company_name: company,
    job_title: title,
    location: location,
    redirect_url: url,
    job_employment_type: job.job_employment_type || job.type || 'Full-time',
    portal: 'Official Company Web',
  };
}

function JobCard({ job, index, onApplyClick, isApplied }) {
  const j = normalizeJob(job);
  const branding = getCompanyBranding(j.company_name);

  return (
    <article className="tw-property-card" style={{ animationDelay: `${index * 60}ms` }}>
      {/* Branded Company Header Banner */}
      <div
        className="tw-property-card__thumb position-relative d-flex flex-column align-items-center justify-content-center p-3 text-white"
        style={{ background: branding.gradient, minHeight: '140px' }}
      >
        <div
          className="d-flex align-items-center justify-content-center rounded-3 shadow mb-1"
          style={{
            width: '42px',
            height: '42px',
            background: branding.logoBg,
            color: branding.logoColor,
            fontWeight: 800,
            fontSize: '1.05rem',
            border: '2px solid rgba(255, 255, 255, 0.4)',
          }}
        >
          {branding.abbr}
        </div>
        <div className="fw-bold fs-5 text-white text-center text-truncate w-100 px-2" title={j.company_name}>
          {j.company_name}
        </div>
        <div className="badge bg-white bg-opacity-25 text-white mt-1" style={{ fontSize: '0.68rem', fontWeight: 500 }}>
          Official Direct Opening
        </div>
        <span className="tw-property-card__badge">{j.job_employment_type}</span>
      </div>

      <div className="tw-property-card__body d-flex flex-column justify-content-between" style={{ minHeight: '265px' }}>
        <div>
          <div className="d-flex justify-content-between align-items-center mb-2">
            <p className="tw-property-card__category mb-0">{j.role_category}</p>
            <span className="badge bg-success-subtle text-success border border-success px-2 py-1" style={{ fontSize: '0.7rem', fontWeight: 600 }}>
              ✓ Official Web
            </span>
          </div>

          <h4 className="tw-property-card__title mb-2" title={j.job_title} style={{ minHeight: '44px' }}>
            {j.job_title}
          </h4>

          <div className="d-flex align-items-center gap-2 mb-2">
            <span className="badge bg-primary text-white px-2 py-1 fw-bold fs-6 d-inline-flex align-items-center gap-1 shadow-sm">
              <Building2 size={13} />
              {j.company_name}
            </span>
            <span className="badge bg-light text-secondary border">Direct Hire</span>
          </div>

          <p className="tw-property-card__location text-muted mb-3">
            <MapPin size={14} className="me-1 text-danger" style={{ display: 'inline' }} />
            {j.location}
          </p>
        </div>

        <div className="tw-property-card__footer mt-3 d-flex flex-column gap-2">
          {isApplied ? (
            <button
              type="button"
              className="btn btn-sm btn-success w-100 d-inline-flex align-items-center justify-content-center gap-1"
              disabled
            >
              <CheckCircle size={14} />
              <span>✓ Applied &amp; Tracked</span>
            </button>
          ) : (
            <button
              type="button"
              className="btn btn-sm btn-primary tw-btn-primary w-100 d-inline-flex align-items-center justify-content-center gap-1 shadow-sm"
              onClick={() => onApplyClick(j)}
            >
              <Send size={13} />
              <span>Apply with Resume</span>
            </button>
          )}

          {j.redirect_url && (
            <a
              href={j.redirect_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-sm btn-outline-secondary w-100 d-inline-flex align-items-center justify-content-center gap-1 text-decoration-none"
              style={{ fontSize: '0.78rem' }}
            >
              <span>Visit {j.company_name} Official Career Web</span>
              <ExternalLink size={12} />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}

function RoleJobGroup({ roleName, jobs, onApplyClick, appliedJobs = {} }) {
  return (
    <section className="tw-listing-group mb-4">
      <div className="tw-listing-group__head d-flex justify-content-between align-items-center mb-3">
        <h3 className="tw-listing-group__title mb-0">{roleName}</h3>
        <span className="tw-listing-group__count badge bg-light text-dark border">{(jobs || []).length} openings</span>
      </div>
      <div className="row g-4">
        {(jobs || []).length > 0 ? (
          jobs.map((job, i) => {
            const jNorm = normalizeJob(job);
            const key = `${jNorm.company_name.toLowerCase()}::${jNorm.job_title.toLowerCase()}`;
            const isApplied = Boolean(appliedJobs[key]);
            return (
              <div key={`${roleName}-${job.job_title}-${i}`} className="col-md-6 col-lg-4 col-xl-3">
                <JobCard
                  job={job}
                  index={i}
                  onApplyClick={onApplyClick}
                  isApplied={isApplied}
                />
              </div>
            );
          })
        ) : (
          <div className="col-12">
            <div className="tw-listing-empty p-4 text-center text-muted border rounded bg-light">
              <p className="mb-2">No matching openings for this role with the selected filters.</p>
              <div className="d-flex flex-wrap justify-content-center gap-2 mt-3">
                <a
                  href={`https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(roleName)}&location=India`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-primary"
                >
                  Search on LinkedIn
                </a>
                <a
                  href={`https://www.naukri.com/${encodeURIComponent(roleName).toLowerCase().replace(/[^a-z0-9]+/g, '-')}-jobs-in-india`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-secondary"
                >
                  Search on Naukri
                </a>
                <a
                  href={`https://in.indeed.com/jobs?q=${encodeURIComponent(roleName)}&l=India`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-info"
                >
                  Search on Indeed
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default function LiveJobOpenings({
  recommendedRoles = [],
  jobsByRole = {},
  jobsMessage = null,
  jobsCount = 0,
  loading = false,
  title = "Live Job Openings — India",
  subtitle = null,
  candidateProfile = {},
  onOpenApplications = null,
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCity, setSelectedCity] = useState('All');
  const [selectedRoleTab, setSelectedRoleTab] = useState('All');
  const [activeApplyJob, setActiveApplyJob] = useState(null);
  const [appliedJobs, setAppliedJobs] = useState({});

  useEffect(() => {
    apiService.getAppliedJobs()
      .then((res) => {
        if (res?.applied_keys && Array.isArray(res.applied_keys)) {
          const map = {};
          res.applied_keys.forEach((k) => { map[k] = true; });
          setAppliedJobs((prev) => ({ ...prev, ...map }));
        }
      })
      .catch(() => {});
  }, []);

  const handleApplySuccess = (job, res) => {
    const key = `${(job.company_name || '').toLowerCase()}::${(job.job_title || '').toLowerCase()}`;
    setAppliedJobs((prev) => ({ ...prev, [key]: true }));
  };

  const roleOrder = useMemo(() => {
    if ((recommendedRoles || []).length > 0) return recommendedRoles;
    return Object.keys(jobsByRole || {});
  }, [recommendedRoles, jobsByRole]);

  const allJobsFlat = useMemo(() => {
    const list = [];
    Object.entries(jobsByRole || {}).forEach(([role, jobs]) => {
      (jobs || []).forEach((j) => {
        list.push({ ...j, role_category: j.role_category || role });
      });
    });
    return list;
  }, [jobsByRole]);

  const cities = useMemo(() => {
    const set = new Set();
    allJobsFlat.forEach((j) => {
      const loc = (j.location || '').toLowerCase();
      if (loc.includes('bengaluru') || loc.includes('bangalore')) set.add('Bengaluru');
      else if (loc.includes('hyderabad')) set.add('Hyderabad');
      else if (loc.includes('pune')) set.add('Pune');
      else if (loc.includes('mumbai')) set.add('Mumbai');
      else if (loc.includes('gurugram') || loc.includes('gurgaon') || loc.includes('noida') || loc.includes('delhi')) set.add('Delhi NCR');
      else if (loc.includes('chennai')) set.add('Chennai');
      else if (loc.includes('remote')) set.add('Remote');
    });
    return ['All', ...Array.from(set)];
  }, [allJobsFlat]);

  const filteredJobsByRole = useMemo(() => {
    const out = {};
    const query = searchQuery.trim().toLowerCase();

    roleOrder.forEach((role) => {
      if (selectedRoleTab !== 'All' && selectedRoleTab !== role) return;

      const rawList = jobsByRole[role] || [];
      const filtered = rawList.filter((job) => {
        const titleMatch = !query || (job.job_title || '').toLowerCase().includes(query) || (job.company_name || '').toLowerCase().includes(query) || (job.role_category || '').toLowerCase().includes(query);
        const cityMatch = selectedCity === 'All' || (job.location || '').toLowerCase().includes(selectedCity.toLowerCase());
        return titleMatch && cityMatch;
      });
      out[role] = filtered;
    });
    return out;
  }, [jobsByRole, roleOrder, searchQuery, selectedCity, selectedRoleTab]);

  const totalFilteredCount = useMemo(() => {
    return Object.values(filteredJobsByRole).reduce((sum, l) => sum + (l?.length || 0), 0);
  }, [filteredJobsByRole]);

  const totalJobs = jobsCount ?? allJobsFlat.length;

  return (
    <section className="tw-listings" id="live-jobs">
      <div className="tw-section-head text-center mb-4">
        <div className="d-inline-flex align-items-center gap-1 tw-section-label mb-2">
          <Sparkles size={16} />
          <span>India Job Network</span>
        </div>
        <h3 className="tw-section-title">{title}</h3>
        <p className="tw-section-sub">
          {subtitle || (totalJobs > 0
            ? `${totalJobs} verified openings matched across LinkedIn, Naukri, Indeed & top employers`
            : 'Real-time verified India job search')}
        </p>
        {onOpenApplications && (
          <div className="mt-2">
            <button
              type="button"
              className="btn btn-sm btn-outline-primary d-inline-flex align-items-center gap-1 shadow-sm px-3"
              style={{ borderRadius: '20px' }}
              onClick={onOpenApplications}
            >
              <Briefcase size={14} />
              <span>Applied Jobs Tracker</span>
              <span className="badge bg-primary text-white ms-1 rounded-pill" style={{ fontSize: '0.72rem' }}>
                {Object.keys(appliedJobs).length}
              </span>
            </button>
          </div>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="tw-job-filter-bar mb-4 p-3 bg-white border rounded shadow-sm">
        <div className="row g-2 align-items-center">
          <div className="col-md-5">
            <div className="input-group">
              <span className="input-group-text bg-transparent border-end-0">
                <Search size={16} className="text-muted" />
              </span>
              <input
                type="text"
                className="form-control border-start-0"
                placeholder="Search job title or company..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-4">
            <div className="input-group">
              <span className="input-group-text bg-transparent border-end-0">
                <Filter size={16} className="text-muted" />
              </span>
              <select
                className="form-select border-start-0"
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
              >
                <option value="All">All Locations (India &amp; Remote)</option>
                {cities.filter((c) => c !== 'All').map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="col-md-3 text-md-end text-muted small">
            <span>Showing <strong>{totalFilteredCount}</strong> openings</span>
          </div>
        </div>

        {/* Role Chips */}
        {roleOrder.length > 1 && (
          <div className="d-flex flex-wrap gap-2 mt-3 pt-2 border-top">
            <span className="small text-muted align-self-center me-1">Role:</span>
            <button
              type="button"
              className={`btn btn-sm ${selectedRoleTab === 'All' ? 'btn-primary' : 'btn-outline-secondary'}`}
              onClick={() => setSelectedRoleTab('All')}
            >
              All Roles ({totalJobs})
            </button>
            {roleOrder.map((r) => (
              <button
                key={r}
                type="button"
                className={`btn btn-sm ${selectedRoleTab === r ? 'btn-primary' : 'btn-outline-secondary'}`}
                onClick={() => setSelectedRoleTab(r)}
              >
                {r} ({(jobsByRole[r] || []).length})
              </button>
            ))}
          </div>
        )}
      </div>

      {loading && (
        <p className="tw-listing-notice tw-listing-notice--loading" role="status">
          Fetching live career listings for your roles…
        </p>
      )}

      {!loading && jobsMessage && (
        <p className="tw-listing-notice" role="status">{jobsMessage}</p>
      )}

      {Object.keys(filteredJobsByRole).map((roleName) => (
        <RoleJobGroup
          key={roleName}
          roleName={roleName}
          jobs={filteredJobsByRole[roleName] || []}
          onApplyClick={setActiveApplyJob}
          appliedJobs={appliedJobs}
        />
      ))}

      {activeApplyJob && (
        <ApplyModal
          job={activeApplyJob}
          candidateProfile={candidateProfile}
          onClose={() => setActiveApplyJob(null)}
          onApplySuccess={handleApplySuccess}
          onViewApplications={onOpenApplications}
        />
      )}
    </section>
  );
}
