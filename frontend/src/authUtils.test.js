import { formatAuthError, getApiOrigin } from './authUtils';

describe('authUtils', () => {
  test('returns default API origin when env var is not set', () => {
    const origin = getApiOrigin();
    expect(origin).toBe('http://127.0.0.1:8000');
  });

  test('formats network error with helpful backend running guidance', () => {
    const err = { code: 'ERR_NETWORK', message: 'Network Error' };
    const formatted = formatAuthError(err);
    expect(formatted).toContain('Unable to reach the server');
    expect(formatted).toContain('backend server is running');
  });

  test('formats string detail error from backend', () => {
    const err = { response: { data: { detail: 'Password must be at least 8 characters long.' } } };
    expect(formatAuthError(err)).toBe('Password must be at least 8 characters long.');
  });

  test('formats array detail error from FastAPI Pydantic validation', () => {
    const err = {
      response: {
        data: {
          detail: [{ msg: 'Field required' }, { msg: 'Value is invalid' }],
        },
      },
    };
    expect(formatAuthError(err)).toBe('Field required; Value is invalid');
  });
});
