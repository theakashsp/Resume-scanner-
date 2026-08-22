import React, { useState } from 'react';
import axios from 'axios';
import { X, UserPlus, LogIn } from 'lucide-react';

function getApiOrigin() {
  const raw = process.env.REACT_APP_API_URL;
  if (raw != null && String(raw).trim() !== '') {
    return String(raw).trim().replace(/\/$/, '');
  }
  return 'http://127.0.0.1:8000';
}

function formatAuthError(err) {
  const data = err.response?.data;
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((x) => x?.msg || x).filter(Boolean).join('; ') || 'Request failed';
  }
  return err.message || 'Something went wrong. Please try again.';
}

export default function AuthModal({ mode, onClose, onAuthSuccess }) {
  const [tab, setTab] = useState(mode === 'register' ? 'register' : 'signin');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [demoOtp, setDemoOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');

  const api = getApiOrigin();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setInfo('');
    setLoading(true);
    try {
      await axios.post(`${api}/api/auth/register`, {
        name: name.trim(),
        phone: phone.trim(),
        password,
      });
      setInfo('Account created. Sign in with your phone number and OTP.');
      setTab('signin');
      setPassword('');
      setOtpSent(false);
      setDemoOtp('');
    } catch (err) {
      setError(formatAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleRequestOtp = async (e) => {
    e.preventDefault();
    setError('');
    setInfo('');
    setLoading(true);
    try {
      const { data } = await axios.post(`${api}/api/auth/otp/request`, {
        phone: phone.trim(),
      });
      setOtpSent(true);
      setDemoOtp(data.demo_otp || '');
      setInfo(data.message || 'OTP sent. Enter the 6-digit code.');
    } catch (err) {
      setError(formatAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const { data } = await axios.post(`${api}/api/auth/otp/verify`, {
        phone: phone.trim(),
        otp: otp.trim(),
      });
      onAuthSuccess?.({ token: data.token, user: data.user });
      onClose?.();
    } catch (err) {
      setError(formatAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tw-auth-overlay" role="dialog" aria-modal="true" onClick={onClose}>
      <div className="tw-auth-modal" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="tw-auth-modal__close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        <div className="tw-auth-tabs">
          <button
            type="button"
            className={`tw-auth-tab ${tab === 'register' ? 'tw-auth-tab--active' : ''}`}
            onClick={() => { setTab('register'); setError(''); setInfo(''); }}
          >
            <UserPlus size={16} /> Register
          </button>
          <button
            type="button"
            className={`tw-auth-tab ${tab === 'signin' ? 'tw-auth-tab--active' : ''}`}
            onClick={() => { setTab('signin'); setError(''); setInfo(''); }}
          >
            <LogIn size={16} /> Sign In
          </button>
        </div>

        {error && <div className="tw-auth-alert tw-auth-alert--error">{error}</div>}
        {info && <div className="tw-auth-alert tw-auth-alert--info">{info}</div>}

        {tab === 'register' ? (
          <form onSubmit={handleRegister} className="tw-auth-form">
            <label>
              Full name
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
                required
                minLength={2}
                autoComplete="name"
              />
            </label>
            <label>
              Phone number
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="10-digit mobile"
                required
                autoComplete="tel"
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Min 6 characters"
                required
                minLength={6}
                autoComplete="new-password"
              />
            </label>
            <button type="submit" className="btn btn-primary tw-btn-primary w-100" disabled={loading}>
              {loading ? 'Creating account…' : 'Create Account'}
            </button>
          </form>
        ) : (
          <form onSubmit={otpSent ? handleVerifyOtp : handleRequestOtp} className="tw-auth-form">
            <label>
              Phone number
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="10-digit mobile"
                required
                autoComplete="tel"
                disabled={otpSent && loading}
              />
            </label>
            {otpSent && (
              <label>
                OTP
                <input
                  type="text"
                  inputMode="numeric"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="6-digit code"
                  required
                  maxLength={6}
                  autoComplete="one-time-code"
                />
              </label>
            )}
            {demoOtp && (
              <p className="tw-auth-demo-otp">
                Demo OTP: <strong>{demoOtp}</strong>
              </p>
            )}
            <button type="submit" className="btn btn-primary tw-btn-primary w-100" disabled={loading}>
              {loading ? 'Please wait…' : otpSent ? 'Verify & Sign In' : 'Send OTP'}
            </button>
            {otpSent && (
              <button
                type="button"
                className="btn tw-btn-outline w-100"
                disabled={loading}
                onClick={() => { setOtpSent(false); setOtp(''); setDemoOtp(''); setInfo(''); }}
              >
                Change phone number
              </button>
            )}
          </form>
        )}
      </div>
    </div>
  );
}
