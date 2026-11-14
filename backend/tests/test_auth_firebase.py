from __future__ import annotations

import time
import pytest
from unittest.mock import MagicMock, patch
import auth_store
import firebase_service


class FakeDocRef:
    def __init__(self, col, doc_id: str):
        self.col = col
        self.id = str(doc_id)

    def get(self):
        doc_data = self.col.data.get(self.id)
        mock = MagicMock()
        mock.exists = doc_data is not None
        mock.to_dict.return_value = dict(doc_data) if doc_data is not None else None
        mock.id = self.id
        return mock

    def set(self, data):
        self.col.data[self.id] = dict(data)

    def delete(self):
        self.col.data.pop(self.id, None)


class FakeFirestoreCollection:
    def __init__(self):
        self.data: dict[str, dict] = {}

    def document(self, doc_id: str):
        return FakeDocRef(self, str(doc_id))

    def add(self, data):
        doc_id = str(len(self.data) + 1)
        self.data[doc_id] = dict(data)
        return None, FakeDocRef(self, doc_id)

    def stream(self):
        for doc_id, data in self.data.items():
            mock = MagicMock()
            mock.id = doc_id
            mock.to_dict.return_value = dict(data)
            yield mock

    def where(self, field: str, op: str, value: str):
        mock_query = MagicMock()
        def _stream():
            for doc_id, data in self.data.items():
                if data.get(field) == value:
                    mock = MagicMock()
                    mock.id = doc_id
                    mock.to_dict.return_value = dict(data)
                    mock.reference = FakeDocRef(self, doc_id)
                    yield mock
        mock_query.stream = _stream
        mock_query.limit.return_value = mock_query
        return mock_query


@pytest.fixture
def mock_firebase_collections():
    users_col = FakeFirestoreCollection()
    sessions_col = FakeFirestoreCollection()
    apps_col = FakeFirestoreCollection()
    analyses_col = FakeFirestoreCollection()
    failed_col = FakeFirestoreCollection()

    with patch("firebase_service.is_firebase_configured", return_value=True), \
         patch("firebase_service.is_firestore_connected", return_value=True), \
         patch("firebase_service.get_users_col", return_value=users_col), \
         patch("firebase_service.get_sessions_col", return_value=sessions_col), \
         patch("firebase_service.get_applications_col", return_value=apps_col), \
         patch("firebase_service.get_analyses_col", return_value=analyses_col), \
         patch("firebase_service.get_failed_logins_col", return_value=failed_col), \
         patch("auth_store.is_firebase_active", return_value=True):
        yield {
            "users": users_col,
            "sessions": sessions_col,
            "applications": apps_col,
            "analyses": analyses_col,
            "failed": failed_col,
        }


def test_firebase_register_and_login_flow(mock_firebase_collections):
    users = mock_firebase_collections["users"]
    sessions = mock_firebase_collections["sessions"]

    # 1. Register a new user in Firebase Firestore
    registered = auth_store.register_user(
        name="Firebase Engineer",
        email="firebase.dev@example.com",
        password="ValidPassword123!",
        phone="9876543210",
    )
    assert registered["name"] == "Firebase Engineer"
    assert registered["email"] == "firebase.dev@example.com"
    assert registered["phone"] == "9876543210"

    # Verify user was saved in Firestore users collection
    assert "firebase.dev@example.com" in users.data
    stored = users.data["firebase.dev@example.com"]
    assert stored["email"] == "firebase.dev@example.com"
    assert stored["password_hash"] != "ValidPassword123!"  # Hashed
    assert len(stored["salt"]) > 0

    # 2. Reject duplicate email in Firestore
    with pytest.raises(ValueError) as exc:
        auth_store.register_user(
            name="Another Firebase",
            email="firebase.dev@example.com",
            password="AnotherPassword123!",
        )
    assert "already exists" in str(exc.value)

    # 3. Log in with wrong password fails
    with pytest.raises(ValueError) as exc:
        auth_store.login_user("firebase.dev@example.com", "WrongPassword!")
    assert "Invalid email or password" in str(exc.value)

    # 4. Log in with correct password succeeds and creates session doc in Firestore
    login_res = auth_store.login_user("firebase.dev@example.com", "ValidPassword123!")
    assert "token" in login_res
    assert login_res["user"]["email"] == "firebase.dev@example.com"
    token = login_res["token"]

    # Verify session is persisted in Firestore user_sessions collection
    assert token in sessions.data
    assert sessions.data[token]["email"] == "firebase.dev@example.com"

    # 5. Retrieve user by session token from Firestore
    user_data = auth_store.get_user_by_token(token)
    assert user_data is not None
    assert user_data["name"] == "Firebase Engineer"
    assert user_data["email"] == "firebase.dev@example.com"

    # 6. Logout terminates session in Firestore
    auth_store.logout(token)
    assert token not in sessions.data
    assert auth_store.get_user_by_token(token) is None


def test_firebase_applications_crud(mock_firebase_collections):
    # Test saving an application to Firestore
    app_record = {
        "id": "app-test-123",
        "job_key": "testcorp::backend engineer",
        "company_name": "TestCorp",
        "job_title": "Backend Engineer",
        "candidate_email": "candidate@example.com",
        "candidate_name": "Test Candidate",
        "status": "applied",
        "created_at": time.time(),
        "recruiter_replies": [],
    }
    saved = firebase_service.save_application_to_firestore(app_record)
    assert saved is True

    # Retrieve applications
    apps = firebase_service.get_applications_from_firestore("candidate@example.com")
    assert len(apps) == 1
    assert apps[0]["company_name"] == "TestCorp"
    assert apps[0]["status"] == "applied"

    # Update application with recruiter reply
    reply = {
        "id": "reply-1",
        "message": "Thanks for applying! We'd like to schedule an interview.",
        "recruiter_name": "HR Team",
        "created_at": time.time(),
        "new_status": "in_review",
    }
    updated = firebase_service.update_application_reply_in_firestore("app-test-123", reply, "in_review")
    assert updated is not None
    assert updated["status"] == "in_review"
    assert len(updated["recruiter_replies"]) == 1
