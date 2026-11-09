from __future__ import annotations

import time
import pytest
from unittest.mock import MagicMock, patch
import auth_store
import mongo


class FakeMongoCollection:
    def __init__(self):
        self.docs = []

    def find_one(self, query):
        for doc in self.docs:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return dict(doc)
        return None

    def insert_one(self, doc):
        stored = dict(doc)
        self.docs.append(stored)
        return MagicMock(inserted_id=str(len(self.docs)))

    def delete_one(self, query):
        initial_len = len(self.docs)
        self.docs = [d for d in self.docs if not all(d.get(k) == v for k, v in query.items())]
        return MagicMock(deleted_count=initial_len - len(self.docs))


@pytest.fixture
def mock_mongo_collections():
    users_col = FakeMongoCollection()
    sessions_col = FakeMongoCollection()
    analyses_col = FakeMongoCollection()
    failed_col = FakeMongoCollection()

    with patch("mongo.is_mongo_configured", return_value=True), \
         patch("mongo.get_users_col", return_value=users_col), \
         patch("mongo.get_sessions_col", return_value=sessions_col), \
         patch("mongo.get_analyses_col", return_value=analyses_col), \
         patch("mongo.get_failed_logins_col", return_value=failed_col), \
         patch("auth_store.is_mongo_active", return_value=True):
        yield {
            "users": users_col,
            "sessions": sessions_col,
            "analyses": analyses_col,
            "failed": failed_col,
        }


def test_mongo_register_and_login_flow(mock_mongo_collections):
    users = mock_mongo_collections["users"]
    sessions = mock_mongo_collections["sessions"]

    # 1. Register a new user
    registered = auth_store.register_user(
        name="Mongo Engineer",
        email="mongo.dev@example.com",
        password="ValidPassword123!",
        phone="9876543210",
    )
    assert registered["name"] == "Mongo Engineer"
    assert registered["email"] == "mongo.dev@example.com"
    assert registered["phone"] == "9876543210"

    # Verify user was saved in MongoDB users collection
    assert len(users.docs) == 1
    stored = users.docs[0]
    assert stored["email"] == "mongo.dev@example.com"
    assert stored["password_hash"] != "ValidPassword123!"  # Hashed
    assert len(stored["salt"]) > 0

    # 2. Reject duplicate email in MongoDB
    with pytest.raises(ValueError) as exc:
        auth_store.register_user(
            name="Another Mongo",
            email="mongo.dev@example.com",
            password="AnotherPassword123!",
        )
    assert "already exists" in str(exc.value)

    # 3. Log in with wrong password fails
    with pytest.raises(ValueError) as exc:
        auth_store.login_user("mongo.dev@example.com", "WrongPassword!")
    assert "Invalid email or password" in str(exc.value)

    # 4. Log in with correct password succeeds and creates session doc
    login_res = auth_store.login_user("mongo.dev@example.com", "ValidPassword123!")
    assert "token" in login_res
    assert login_res["user"]["email"] == "mongo.dev@example.com"
    token = login_res["token"]

    # Verify session is persisted in MongoDB sessions collection
    assert len(sessions.docs) == 1
    assert sessions.docs[0]["token"] == token
    assert sessions.docs[0]["email"] == "mongo.dev@example.com"

    # 5. Retrieve user by session token from MongoDB
    user_data = auth_store.get_user_by_token(token)
    assert user_data is not None
    assert user_data["name"] == "Mongo Engineer"
    assert user_data["email"] == "mongo.dev@example.com"

    # 6. Logout terminates session in MongoDB
    auth_store.logout(token)
    assert len(sessions.docs) == 0
    assert auth_store.get_user_by_token(token) is None

