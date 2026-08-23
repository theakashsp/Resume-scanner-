export function getApiOrigin() {
  const raw = process.env.REACT_APP_API_URL;
  if (raw != null && String(raw).trim() !== '') {
    return String(raw).trim().replace(/\/$/, '');
  }
  return 'http://127.0.0.1:8000';
}

export function formatAuthError(err) {
  const data = err.response?.data;
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((x) => x?.msg || x).filter(Boolean).join('; ') || 'Request failed';
  }
  return err.message || 'Something went wrong. Please try again.';
}
