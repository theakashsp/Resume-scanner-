# ==============================================================================
# TECH STACK: [Firebase Admin SDK] - Cloud Firestore & Firebase Cloud Storage
# Replaces MongoDB & AWS S3 with Google Cloud Firebase infrastructure.
# Provides:
#  1. Cloud Firestore: Scalable NoSQL document store for Users, Sessions,
#     Job Applications, Analysis History, and Security Records.
#  2. Firebase Cloud Storage: Secure bucket storage for candidate resumes & PDF reports
#     with signed expiring download URLs.
#  3. Graceful Local Fallback: Fully functional even when Firebase keys are absent.
# ==============================================================================
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from logger import logger

# Lazy-loaded Firebase Admin SDK singletons
_firebase_app: Any = None
_firestore_client: Any = None
_storage_bucket: Any = None
_is_initialized: bool = False

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    _FIREBASE_AVAILABLE = True
except ImportError:
    firebase_admin = None
    credentials = None
    firestore = None
    storage = None
    _FIREBASE_AVAILABLE = False


def _resolve_credentials() -> Any | None:
    """
    Resolves Firebase service account credentials from:
    1. FIREBASE_CREDENTIALS_JSON: Inline JSON string (ideal for Render, Railway, Vercel)
    2. FIREBASE_CREDENTIALS_PATH / FIREBASE_SERVICE_ACCOUNT_KEY: File path to serviceAccountKey.json
    3. GOOGLE_APPLICATION_CREDENTIALS: Standard GCP environment variable
    """
    if not _FIREBASE_AVAILABLE:
        return None

    # Option 1: Inline JSON string (e.g. from Cloud platform environment variables)
    inline_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "").strip()
    if inline_json:
        try:
            cert_dict = json.loads(inline_json)
            logger.info("[Firebase] Loaded credentials from FIREBASE_CREDENTIALS_JSON environment variable.")
            return credentials.Certificate(cert_dict)
        except Exception as exc:
            logger.error(f"[Firebase] Failed to parse FIREBASE_CREDENTIALS_JSON: {exc}")

    # Option 2: Path to JSON service account file
    for env_var in ("FIREBASE_CREDENTIALS_PATH", "FIREBASE_SERVICE_ACCOUNT_KEY", "GOOGLE_APPLICATION_CREDENTIALS"):
        path_str = os.getenv(env_var, "").strip()
        if path_str:
            path = Path(path_str)
            if not path.is_absolute():
                # Check relative to backend directory or workspace root
                candidate_paths = [
                    Path(__file__).resolve().parent / path_str,
                    Path.cwd() / path_str,
                    Path.cwd() / "backend" / path_str,
                ]
                for p in candidate_paths:
                    if p.is_file():
                        path = p
                        break
            if path.is_file():
                try:
                    logger.info(f"[Firebase] Loaded credentials from file: {path}")
                    return credentials.Certificate(str(path))
                except Exception as exc:
                    logger.error(f"[Firebase] Error loading certificate file '{path}': {exc}")

    # Option 3: Default application credentials (e.g., when hosted on Google Cloud Run)
    try:
        return credentials.ApplicationDefault()
    except Exception:
        pass

    return None


def init_firebase() -> bool:
    """
    Initializes the Firebase Admin SDK singleton.
    Safe to call multiple times (idempotent).
    """
    global _firebase_app, _firestore_client, _storage_bucket, _is_initialized
    if _is_initialized:
        return _firebase_app is not None

    if not _FIREBASE_AVAILABLE:
        logger.info("[Firebase] firebase-admin package is not installed. Using local storage fallback.")
        _is_initialized = True
        return False

    cred = _resolve_credentials()
    if cred is None:
        logger.info("[Firebase] No Firebase credentials provided. Operating in local JSON storage mode.")
        _is_initialized = True
        return False

    project_id = os.getenv("FIREBASE_PROJECT_ID", "").strip() or None
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET", "").strip() or None

    options: dict[str, Any] = {}
    if project_id:
        options["projectId"] = project_id
    if bucket_name:
        options["storageBucket"] = bucket_name

    try:
        # Check if already initialized by another module
        try:
            _firebase_app = firebase_admin.get_app()
        except ValueError:
            _firebase_app = firebase_admin.initialize_app(cred, options=options or None)

        logger.info(f"[Firebase] Successfully initialized Firebase Admin SDK (Project: {project_id or 'default'}).")

        # Initialize Firestore client
        try:
            _firestore_client = firestore.client()
            logger.info("[Firebase] Cloud Firestore client connected.")
        except Exception as f_err:
            logger.warning(f"[Firebase] Could not initialize Firestore client: {f_err}")
            _firestore_client = None

        # Initialize Storage bucket
        if bucket_name:
            try:
                _storage_bucket = storage.bucket(bucket_name)
                logger.info(f"[Firebase] Cloud Storage bucket '{bucket_name}' initialized.")
            except Exception as s_err:
                logger.warning(f"[Firebase] Could not connect to Storage bucket '{bucket_name}': {s_err}")
                _storage_bucket = None

        _is_initialized = True
        return True
    except Exception as exc:
        logger.error(f"[Firebase] Initialization failed: {exc}")
        _firebase_app = None
        _firestore_client = None
        _storage_bucket = None
        _is_initialized = True
        return False


def is_firebase_configured() -> bool:
    """Returns True if Firebase has been initialized with valid credentials."""
    if not _is_initialized:
        init_firebase()
    return _firebase_app is not None


def get_firestore_client() -> Any | None:
    """Returns the Cloud Firestore client or None if unconfigured."""
    if not _is_initialized:
        init_firebase()
    return _firestore_client


def is_firestore_connected() -> bool:
    """Verifies live Firestore connectivity."""
    db = get_firestore_client()
    if db is None:
        return False
    try:
        # Lightweight check: access collections metadata without heavy reads
        _ = list(db.collections())
        return True
    except Exception as exc:
        logger.warning(f"[Firebase] Firestore health probe failed: {exc}")
        return False


def get_project_id() -> str | None:
    """Returns the configured Firebase Project ID."""
    custom = os.getenv("FIREBASE_PROJECT_ID", "").strip()
    if custom:
        return custom
    if _firebase_app is not None:
        return getattr(_firebase_app, "project_id", None)
    return None


def get_storage_bucket_name() -> str | None:
    """Returns the configured Firebase Storage bucket name."""
    return os.getenv("FIREBASE_STORAGE_BUCKET", "").strip() or None


# ==============================================================================
# FIRESTORE DATA COLLECTIONS & CRUD OPERATIONS
# Collections:
#  - users: User registration & account profiles
#  - user_sessions: Active login tokens & session expiration
#  - applications: 1-Click Smart Apply job submissions & candidate status
#  - analysis_records: Resume scans, ATS scores, and identified skill gaps
#  - failed_logins: Brute-force lockout and rate limiting tracking
# ==============================================================================

def get_users_col() -> Any | None:
    db = get_firestore_client()
    return db.collection("users") if db is not None else None


def get_sessions_col() -> Any | None:
    db = get_firestore_client()
    return db.collection("user_sessions") if db is not None else None


def get_applications_col() -> Any | None:
    db = get_firestore_client()
    return db.collection("applications") if db is not None else None


def get_analyses_col() -> Any | None:
    db = get_firestore_client()
    return db.collection("analysis_records") if db is not None else None


def get_failed_logins_col() -> Any | None:
    db = get_firestore_client()
    return db.collection("failed_logins") if db is not None else None


# ------------------------------------------------------------------------------
# Firestore Operations for Job Applications
# ------------------------------------------------------------------------------
def save_application_to_firestore(app_record: dict[str, Any]) -> bool:
    """Saves a candidate job application document into Firestore."""
    col = get_applications_col()
    if col is None:
        return False
    try:
        doc_id = str(app_record.get("id") or app_record.get("job_key") or f"{app_record.get('candidate_email')}-{int(time.time())}")
        doc_data = dict(app_record)
        doc_data["id"] = doc_id
        col.document(doc_id).set(doc_data)
        logger.info(f"[Firebase] Stored application '{doc_id}' in Firestore for {app_record.get('candidate_email')}")
        return True
    except Exception as exc:
        logger.error(f"[Firebase] Error saving application to Firestore: {exc}")
        return False


def get_applications_from_firestore(candidate_email: str | None = None) -> list[dict[str, Any]]:
    """Retrieves job applications from Firestore, optionally filtered by candidate email."""
    col = get_applications_col()
    if col is None:
        return []
    try:
        if candidate_email:
            # Case-insensitive / normalized lookup
            email_clean = candidate_email.strip().lower()
            docs = col.where("candidate_email", "==", email_clean).stream()
        else:
            docs = col.stream()

        results = []
        for d in docs:
            rec = d.to_dict() or {}
            rec["id"] = str(rec.get("id") or d.id)
            results.append(rec)

        # Sort newest first
        results.sort(key=lambda x: float(x.get("created_at") or x.get("applied_at_epoch") or 0), reverse=True)
        return results
    except Exception as exc:
        logger.error(f"[Firebase] Error querying applications from Firestore: {exc}")
        return []


def update_application_reply_in_firestore(app_id: str, reply: dict[str, Any], new_status: str) -> dict[str, Any] | None:
    """Records an employer reply or candidate status update on a job application."""
    col = get_applications_col()
    if col is None:
        return None
    try:
        doc_ref = col.document(app_id)
        doc = doc_ref.get()
        if not doc.exists:
            # Try searching by job_key if doc_id was not the document key
            matches = list(col.where("job_key", "==", app_id).limit(1).stream())
            if not matches:
                return None
            doc_ref = matches[0].reference
            doc = matches[0]

        current = doc.to_dict() or {}
        replies = list(current.get("recruiter_replies") or current.get("replies") or [])
        replies.append(reply)
        current["recruiter_replies"] = replies
        current["status"] = new_status
        current["updated_at"] = time.time()

        doc_ref.set(current)
        current["id"] = doc.id
        logger.info(f"[Firebase] Recorded employer reply for application '{doc.id}' -> status: {new_status}")
        return current
    except Exception as exc:
        logger.error(f"[Firebase] Error updating application in Firestore: {exc}")
        return None


def save_analysis_to_firestore(record: dict[str, Any]) -> bool:
    """Records a resume analysis session in Firestore for analytics and user history."""
    col = get_analyses_col()
    if col is None:
        return False
    try:
        col.add(record)
        return True
    except Exception as exc:
        logger.warning(f"[Firebase] Could not save analysis record to Firestore: {exc}")
        return False


# ==============================================================================
# FIREBASE CLOUD STORAGE (Replaces AWS S3)
# Stores resumes, generated PDF reports, and candidate artifacts securely.
# ==============================================================================
def is_storage_enabled() -> bool:
    """Returns True if Firebase Cloud Storage is configured and ready."""
    if not _is_initialized:
        init_firebase()
    return _storage_bucket is not None


def upload_resume_or_report(
    file_bytes: bytes,
    object_key: str,
    content_type: str = "application/pdf",
    metadata: dict[str, str] | None = None,
) -> str | None:
    """
    Uploads document bytes to Firebase Cloud Storage.
    Returns the cloud storage path if successful, or None if storage is disabled or fails.
    """
    if not is_storage_enabled():
        return None

    try:
        clean_key = object_key.lstrip("/")
        blob = _storage_bucket.blob(clean_key)
        if metadata:
            blob.metadata = {k: str(v) for k, v in metadata.items()}

        blob.upload_from_string(file_bytes, content_type=content_type)
        logger.info(f"[Firebase Storage] Uploaded document to gs://{_storage_bucket.name}/{clean_key}")
        return clean_key
    except Exception as exc:
        logger.error(f"[Firebase Storage] Upload failed for '{object_key}': {exc}")
        return None


def generate_presigned_download_url(
    object_key: str,
    expiration_sec: int = 900,
) -> str | None:
    """
    Generates a secure, short-lived V4 signed URL for downloading private documents
    directly from Firebase Cloud Storage without public bucket exposure.
    """
    if not is_storage_enabled():
        return None

    try:
        from datetime import timedelta
        clean_key = object_key.lstrip("/")
        blob = _storage_bucket.blob(clean_key)
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=expiration_sec),
            method="GET",
        )
        return url
    except Exception as exc:
        logger.error(f"[Firebase Storage] Error generating signed download URL for '{object_key}': {exc}")
        return None


def delete_object(object_key: str) -> bool:
    """Deletes an object from Firebase Cloud Storage."""
    if not is_storage_enabled():
        return False

    try:
        clean_key = object_key.lstrip("/")
        blob = _storage_bucket.blob(clean_key)
        blob.delete()
        logger.info(f"[Firebase Storage] Deleted object '{clean_key}'")
        return True
    except Exception as exc:
        logger.error(f"[Firebase Storage] Error deleting object '{object_key}': {exc}")
        return False
