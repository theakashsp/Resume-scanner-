import React, { useState } from 'react';
import axios from 'axios';
import { LogIn, Phone, ShieldCheck, ArrowLeft } from 'lucide-react';
import { formatAuthError, getApiOrigin } from './authUtils';

export default function SignInPage({ onAuthSuccess, onGoRegister, onGoHome }) {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [demoOtp, setDemoOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');

  const api = getApiOrigin();

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
    } catch (err) {
      setError(formatAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="tw-auth-page">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-5 col-md-7">
            <button type="button" className="tw-auth-page__back" onClick={onGoHome}>
              <ArrowLeft size={16} /> Back to Home
            </button>

            <div className="tw-auth-page__card">
              <div className="tw-auth-page__icon">
                <LogIn size={28} />
              </div>
              <span className="tw-section-label">Sign In</span>
              <h1 className="tw-auth-page__title">Welcome Back</h1>
              <p className="tw-auth-page__sub">
                Sign in with your registered phone number and OTP to access Resume Analyzer.
              </p>

              {error && <div className="tw-auth-alert tw-auth-alert--error">{error}</div>}
              {info && <div className="tw-auth-alert tw-auth-alert--info">{info}</div>}

              <form onSubmit={otpSent ? handleVerifyOtp : handleRequestOtp} className="tw-auth-form">
                <label>
                  <Phone size={14} className="me-1" /> Phone number
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
                    <ShieldCheck size={14} className="me-1" /> OTP
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
                    onClick={() => {
                      setOtpSent(false);
                      setOtp('');
                      setDemoOtp('');
                      setInfo('');
                    }}
                  >
                    Change phone number
                  </button>
                )}
              </form>

              <p className="tw-auth-page__footer">
                Don&apos;t have an account?{' '}
                <button type="button" className="tw-auth-page__link" onClick={onGoRegister}>
                  Register here
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
