"""Local phone-based auth: register (name/phone/password) + OTP sign-in."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from pathlib import Path
from typing import Any

_BACKEND_DIR = Path(__file__).resolve().parent
_USERS_FILE = _BACKEND_DIR / "users_data.json"
_OTP_TTL_SEC = 300
_SESSION_TTL_SEC = 60 * 60 * 24 * 14  # 14 days

# phone -> {code, expires_at}
_otp_store: dict[str, dict[str, Any]] = {}
# token -> {phone, expires_at}
_sessions: dict[str, dict[str, Any]] = {}


def normalize_phone(raw: str) -> str:
    digits = "".join(ch for ch in (raw or "") if ch.isdigit())
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    if len(digits) != 10 or digits[0] not in "6789":
        raise ValueError("Enter a valid 10-digit Indian mobile number.")
    return digits


def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return salt, digest


def _verify_password(password: str, salt: str, expected: str) -> bool:
    _, digest = _hash_password(password, salt)
    return hmac.compare_digest(digest, expected)


def _load_users() -> dict[str, Any]:
    if not _USERS_FILE.is_file():
        return {"users": {}}
    try:
        data = json.loads(_USERS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("users"), dict):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return {"users": {}}


def _save_users(data: dict[str, Any]) -> None:
    _USERS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def register_user(name: str, phone: str, password: str) -> dict[str, Any]:
    clean_name = " ".join((name or "").split())
    if len(clean_name) < 2:
        raise ValueError("Name must be at least 2 characters.")
    if len(password or "") < 6:
        raise ValueError("Password must be at least 6 characters.")
    phone_n = normalize_phone(phone)

    data = _load_users()
    if phone_n in data["users"]:
        raise ValueError("This phone number is already registered. Please sign in.")

    salt, pwd_hash = _hash_password(password)
    user = {
        "name": clean_name,
        "phone": phone_n,
        "salt": salt,
        "password_hash": pwd_hash,
        "created_at": int(time.time()),
    }
    data["users"][phone_n] = user
    _save_users(data)
    return {"name": clean_name, "phone": phone_n}


def request_otp(phone: str) -> dict[str, Any]:
    phone_n = normalize_phone(phone)
    data = _load_users()
    if phone_n not in data["users"]:
        raise ValueError("No account found for this phone. Please register first.")

    code = f"{secrets.randbelow(1_000_000):06d}"
    _otp_store[phone_n] = {
        "code": code,
        "expires_at": time.time() + _OTP_TTL_SEC,
        "attempts": 0,
    }
    # No SMS gateway configured — return OTP for local/demo use.
    return {
        "phone": phone_n,
        "message": "OTP generated. Enter the 6-digit code to sign in.",
        "expires_in": _OTP_TTL_SEC,
        "demo_otp": code,
    }


def verify_otp(phone: str, otp: str) -> dict[str, Any]:
    phone_n = normalize_phone(phone)
    entry = _otp_store.get(phone_n)
    if not entry:
        raise ValueError("No OTP requested for this number. Request a new code.")
    if time.time() > float(entry["expires_at"]):
        _otp_store.pop(phone_n, None)
        raise ValueError("OTP expired. Request a new code.")
    entry["attempts"] = int(entry.get("attempts", 0)) + 1
    if entry["attempts"] > 5:
        _otp_store.pop(phone_n, None)
        raise ValueError("Too many attempts. Request a new OTP.")
    if not hmac.compare_digest(str(otp or "").strip(), str(entry["code"])):
        raise ValueError("Invalid OTP. Try again.")

    _otp_store.pop(phone_n, None)
    data = _load_users()
    user = data["users"].get(phone_n)
    if not user:
        raise ValueError("Account not found.")

    token = secrets.token_urlsafe(32)
    _sessions[token] = {"phone": phone_n, "expires_at": time.time() + _SESSION_TTL_SEC}
    return {
        "token": token,
        "user": {"name": user["name"], "phone": phone_n},
    }


def get_user_by_token(token: str | None) -> dict[str, Any] | None:
    if not token:
        return None
    session = _sessions.get(token)
    if not session:
        return None
    if time.time() > float(session["expires_at"]):
        _sessions.pop(token, None)
        return None
    data = _load_users()
    user = data["users"].get(session["phone"])
    if not user:
        return None
    return {"name": user["name"], "phone": user["phone"]}


def logout(token: str | None) -> None:
    if token:
        _sessions.pop(token, None)
