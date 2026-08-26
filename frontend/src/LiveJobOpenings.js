import React, { useState, useMemo } from 'react';
import { MapPin, Briefcase, Building2, ExternalLink, Search, Filter, Sparkles } from 'lucide-react';

function normalizeJob(job) {
  return {
    role_category: job.role_category || '',
    company_name: job.company_name || job.employer_name || 'Company',
    job_title: job.job_title || job.title || 'Open Role',
    location: job.location || 'India',
    redirect_url: job.redirect_url || job.job_apply_link || job.link || '#',
    job_employment_type: job.job_employment_type || job.type || 'Full-time',
    portal: job.portal || (job.redirect_url?.includes('linkedin') ? 'LinkedIn' : job.redirect_url?.includes('naukri') ? 'Naukri' : job.redirect_url?.includes('indeed') ? 'Indeed' : job.redirect_url?.includes('foundit') ? 'Foundit' : 'Direct Apply'),
  };
}

function JobCard({ job, index }) {
  const j = normalizeJob(job);
  const canApply = j.redirect_url && j.redirect_url !== '#';

  return (
    <article className="tw-property-card" style={{ animationDelay: `${index * 60}ms` }}>
      <div className="tw-property-card__thumb">
        <div className="tw-property-card__thumb-inner">
          <Building2 size={32} strokeWidth={1.75} />
        </div>
        <span className="tw-property-card__badge">{j.job_employment_type}</span>
      </div>
      <div className="tw-property-card__body">
        <div className="d-flex justify-content-between align-items-center mb-1">
          <p className="tw-property-card__category mb-0">{j.role_category}</p>
          <span className="badge bg-secondary text-light px-2 py-1" style={{ fontSize: '0.7rem', fontWeight: 500, borderRadius: '4px' }}>
            {j.portal}
          </span>
        </div>
        <h4 className="tw-property-card__title" title={j.job_title}>{j.job_title}</h4>
        <p className="tw-property-card__company">
          <Briefcase size={14} className="me-1 text-primary" />
          {j.company_name}
        </p>
        <p className="tw-property-card__location">
          <MapPin size={14} className="me-1 text-danger" />
          {j.location}
        </p>
        <div className="tw-property-card__footer mt-3">
          {canApply ? (
            <a
              className="btn btn-primary tw-btn-primary btn-sm w-100 d-inline-flex align-items-center justify-content-center gap-1"
              href={j.redirect_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <span>Apply on {j.portal}</span>
              <ExternalLink size={14} />
            </a>
          ) : (
            <span className="tw-property-card__unavailable">Listing unavailable</span>
          )}
        </div>
      </div>
    </article>
  );
}

function RoleJobGroup({ roleName, jobs }) {
  return (
    <section className="tw-listing-group mb-4">
      <div className="tw-listing-group__head d-flex justify-content-between align-items-center mb-3">
        <h3 className="tw-listing-group__title mb-0">{roleName}</h3>
        <span className="tw-listing-group__count badge bg-light text-dark border">{(jobs || []).length} openings</span>
      </div>
      <div className="row g-4">
        {(jobs || []).length > 0 ? (
          jobs.map((job, i) => (
            <div key={`${roleName}-${job.job_title}-${i}`} className="col-md-6 col-lg-4 col-xl-3">
              <JobCard job={job} index={i} />
            </div>
          ))
        ) : (
          <div className="col-12">
            <p className="tw-listing-empty p-4 text-center text-muted border rounded">No matching openings for this role with the selected filters.</p>
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
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCity, setSelectedCity] = useState('All');
  const [selectedRoleTab, setSelectedRoleTab] = useState('All');

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
        />
      ))}
    </section>
  );
}
