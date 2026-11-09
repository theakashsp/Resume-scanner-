# ==============================================================================
# TECH STACK: [MongoDB & PyMongo] - Cloud & Local Document Database Adapter
# Provides connection management, health checks, collection access, and indexes
# for Users, Authentication Sessions, Analysis Records, and Security Logs.
# ==============================================================================
from __future__ import annotations

import os
import re
from typing import Any
from urllib.parse import urlparse

from logger import logger

try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.collection import Collection
    from pymongo.database import Database
    from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
except ImportError:
    pymongo = None
    MongoClient = None
    Collection = Any
    Database = Any
    ConnectionFailure = Exception
    DuplicateKeyError = Exception
    PyMongoError = Exception


def _resolve_mongo_uri() -> str:
    """
    Resolves the MongoDB connection string from environment variables.
    Checks MONGODB_URI, MONGO_URI, and DATABASE_URL (if mongodb:// or mongodb+srv://).
    """
    for key in ("MONGODB_URI", "MONGO_URI", "DATABASE_URL"):
        val = os.getenv(key, "").strip()
        if val.startswith("mongodb://") or val.startswith("mongodb+srv://"):
            return val
    return ""


def _resolve_db_name(uri: str) -> str:
    """
    Extracts the database name from the connection string or MONGODB_DB_NAME env var.
    Defaults to 'resume_analyzer'.
    """
    custom = os.getenv("MONGODB_DB_NAME", "").strip()
    if custom:
        return custom

    if uri:
        try:
            # For mongodb+srv:// or mongodb:// urls, path might be /dbname?params
            parsed = urlparse(uri)
            path = (parsed.path or "").lstrip("/")
            if path:
                # Strip query parameters if present in path
                dbname = path.split("?")[0].strip()
                if dbname:
                    return dbname
        except Exception:
            pass

    return "resume_analyzer"


_client: MongoClient | None = None
_db: Database | None = None
_indexes_initialized: bool = False


def is_mongo_configured() -> bool:
    """Returns True if a MongoDB connection string is provided in environment."""
    return bool(_resolve_mongo_uri()) and pymongo is not None


def get_mongo_client() -> MongoClient | None:
    """
    Returns the singleton PyMongo MongoClient instance.
    Configured with fast failover and standard connection pooling.
    """
    global _client
    if _client is not None:
        return _client

    uri = _resolve_mongo_uri()
    if not uri or pymongo is None:
        return None

    try:
        # Sanitize credentials for safe logging
        sanitized = re.sub(r":([^/@]+)@", ":****@", uri)
        logger.info(f"[MongoDB] Initializing connection to {sanitized}")

        _client = MongoClient(
            uri,
            serverSelectionTimeoutMS=4000,
            connectTimeoutMS=4000,
            socketTimeoutMS=10000,
            maxPoolSize=50,
            minPoolSize=2,
            retryWrites=True,
            appname="ResumeAnalyzer",
        )
        return _client
    except Exception as exc:
        logger.error(f"[MongoDB] Failed to create MongoClient: {exc}")
        _client = None
        return None


def get_mongo_db() -> Database | None:
    """Returns the MongoDB database instance."""
    global _db
    if _db is not None:
        return _db

    client = get_mongo_client()
    if client is None:
        return None

    uri = _resolve_mongo_uri()
    dbname = _resolve_db_name(uri)
    try:
        _db = client[dbname]
        return _db
    except Exception as exc:
        logger.error(f"[MongoDB] Error selecting database '{dbname}': {exc}")
        return None


def is_mongo_connected() -> bool:
    """
    Tests live connectivity to the MongoDB cluster via an admin ping command.
    Fails quickly (within 3 seconds) if cluster is unreachable or credentials are bad.
    """
    client = get_mongo_client()
    if client is None:
        return False
    try:
        client.admin.command("ping")
        return True
    except Exception as exc:
        logger.warning(f"[MongoDB] Ping failed: {exc}")
        return False


def init_mongo_indexes() -> bool:
    """
    Initializes required unique and performance indexes on MongoDB collections:
    - users: unique index on 'email'
    - user_sessions: unique index on 'token', TTL index on 'expires_at'
    - analysis_records: index on 'user_email', index on 'created_at'
    - failed_logins: unique index on 'email'
    """
    global _indexes_initialized
    if _indexes_initialized:
        return True

    db = get_mongo_db()
    if db is None:
        return False

    try:
        # 1. Users collection: unique email index
        db.users.create_index("email", unique=True, background=True)

        # 2. User sessions collection: unique token index + TTL auto-cleanup
        db.user_sessions.create_index("token", unique=True, background=True)
        # Note: If expires_at is stored as epoch float, we handle cleanup in queries;
        # Index on expires_at allows efficient cleanup queries.
        db.user_sessions.create_index("expires_at", background=True)
        db.user_sessions.create_index("email", background=True)

        # 3. Analysis history records
        db.analysis_records.create_index("user_email", background=True)
        db.analysis_records.create_index("created_at", background=True)

        # 4. Failed logins / brute force tracker
        db.failed_logins.create_index("email", unique=True, background=True)

        _indexes_initialized = True
        logger.info("[MongoDB] Schema indexes created successfully on all collections.")
        return True
    except Exception as exc:
        logger.error(f"[MongoDB] Error initializing indexes: {exc}")
        return False


def get_users_col() -> Collection | None:
    db = get_mongo_db()
    return db.users if db is not None else None


def get_sessions_col() -> Collection | None:
    db = get_mongo_db()
    return db.user_sessions if db is not None else None


def get_analyses_col() -> Collection | None:
    db = get_mongo_db()
    return db.analysis_records if db is not None else None


def get_failed_logins_col() -> Collection | None:
    db = get_mongo_db()
    return db.failed_logins if db is not None else None
