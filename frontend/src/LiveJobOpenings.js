import React from 'react';
import { MapPin, Briefcase, Building2 } from 'lucide-react';

function normalizeJob(job) {
  return {
    role_category: job.role_category || '',
    company_name: job.company_name || job.employer_name || 'Company',
    job_title: job.job_title || job.title || 'Open Role',
    location: job.location || 'India',
    redirect_url: job.redirect_url || job.job_apply_link || job.link || '#',
    job_employment_type: job.job_employment_type || job.type || 'Full-time',
  };
}

function JobCard({ job, index }) {
  const j = normalizeJob(job);
  const canApply = j.redirect_url && j.redirect_url !== '#';

  return (
    <article className="tw-property-card" style={{ animationDelay: `${index * 80}ms` }}>
      <div className="tw-property-card__thumb">
        <div className="tw-property-card__thumb-inner">
          <Building2 size={36} strokeWidth={1.5} />
        </div>
        <span className="tw-property-card__badge">{j.job_employment_type}</span>
      </div>
      <div className="tw-property-card__body">
        <p className="tw-property-card__category">{j.role_category}</p>
        <h4 className="tw-property-card__title">{j.job_title}</h4>
        <p className="tw-property-card__company">
          <Briefcase size={14} />
          {j.company_name}
        </p>
        <p className="tw-property-card__location">
          <MapPin size={14} />
          {j.location}
        </p>
        <div className="tw-property-card__footer">
          {canApply ? (
            <a
              className="btn btn-primary tw-btn-primary btn-sm w-100"
              href={j.redirect_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              View &amp; Apply
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
    <section className="tw-listing-group">
      <div className="tw-listing-group__head">
        <h3 className="tw-listing-group__title">{roleName}</h3>
        <span className="tw-listing-group__count">{(jobs || []).length} listings</span>
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
            <p className="tw-listing-empty">No active career listings for this role right now.</p>
          </div>
        )}
      </div>
    </section>
  );
}

export default function LiveJobOpenings({
  recommendedRoles,
  jobsByRole,
  jobsMessage,
  jobsCount,
  loading = false,
}) {
  const roleOrder = (recommendedRoles || []).length
    ? recommendedRoles
    : Object.keys(jobsByRole || {});

  const totalJobs = jobsCount ?? Object.values(jobsByRole || {}).reduce(
    (sum, list) => sum + (list?.length || 0),
    0,
  );

  return (
    <section className="tw-listings" id="live-jobs">
      <div className="tw-section-head text-center mb-4">
        <span className="tw-section-label">Career Listings</span>
        <h3 className="tw-section-title">Live Job Openings — India</h3>
        <p className="tw-section-sub">
          {totalJobs > 0
            ? `${totalJobs} verified openings matched to your recommended career roles`
            : 'Real-time India job search for your profile'}
        </p>
      </div>
      {loading && (
        <p className="tw-listing-notice tw-listing-notice--loading" role="status">
          Fetching live career listings for your roles…
        </p>
      )}
      {!loading && jobsMessage && (
        <p className="tw-listing-notice" role="status">{jobsMessage}</p>
      )}
      {roleOrder.map((roleName) => (
        <RoleJobGroup
          key={roleName}
          roleName={roleName}
          jobs={jobsByRole?.[roleName] || []}
        />
      ))}
    </section>
  );
}
