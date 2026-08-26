export function getApiOrigin() {
  const raw = process.env.REACT_APP_API_URL;
  if (raw != null && String(raw).trim() !== '') {
    return String(raw).trim().replace(/\/$/, '');
  }
  return 'http://127.0.0.1:8000';
}

export function formatAuthError(err) {
  if (err?.code === 'ERR_NETWORK' || err?.message === 'Network Error' || (!err?.response && err?.request)) {
    return `Unable to reach the server at ${getApiOrigin()}. Please make sure the backend server is running.`;
  }
  const data = err?.response?.data;
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((x) => (typeof x === 'string' ? x : x?.msg)).filter(Boolean).join('; ') || 'Request failed';
  }
  if (data?.message) return data.message;
  return err?.message || 'Something went wrong. Please try again.';
}
