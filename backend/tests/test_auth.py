from __future__ import annotations

import time
import pytest
import auth_store


@pytest.fixture(autouse=True)
def cleanup_test_user():
    test_email = "test.engineer@example.com"
    auth_store.reset_failed_attempts(test_email)
    data = auth_store._load_users()
    if test_email in data["users"]:
        data["users"].pop(test_email, None)
        auth_store._save_users(data)
    yield
    if test_email in data["users"]:
        data["users"].pop(test_email, None)
        auth_store._save_users(data)
    auth_store.reset_failed_attempts(test_email)


def test_user_registration_and_password_length_requirement():
    # Passwords shorter than 8 chars must be rejected
    with pytest.raises(ValueError) as exc:
        auth_store.register_user("Test User", "test.engineer@example.com", "short1")
    assert "8 characters" in str(exc.value)

    # Valid registration succeeds
    user = auth_store.register_user("Test User", "test.engineer@example.com", "SecurePass123!", "9876543210")
    assert user["email"] == "test.engineer@example.com"
    assert user["name"] == "Test User"

    # Password is not stored in plaintext
    stored_data = auth_store._load_users()
    stored_user = stored_data["users"]["test.engineer@example.com"]
    assert stored_user["password_hash"] != "SecurePass123!"
    assert len(stored_user["salt"]) > 0


def test_duplicate_registration_rejected():
    auth_store.register_user("Test User", "test.engineer@example.com", "SecurePass123!")
    with pytest.raises(ValueError) as exc:
        auth_store.register_user("Test User", "test.engineer@example.com", "SecurePass123!")
    assert "already exists" in str(exc.value)


def test_login_success_and_token_session():
    auth_store.register_user("Test User", "test.engineer@example.com", "SecurePass123!")

    login_res = auth_store.login_user("test.engineer@example.com", "SecurePass123!")
    assert "token" in login_res
    assert login_res["user"]["email"] == "test.engineer@example.com"

    # Token retrieves active user
    token = login_res["token"]
    user_info = auth_store.get_user_by_token(token)
    assert user_info is not None
    assert user_info["email"] == "test.engineer@example.com"

    # Logout revokes token
    auth_store.logout(token)
    assert auth_store.get_user_by_token(token) is None


def test_brute_force_lockout_protection():
    auth_store.register_user("Test User", "test.engineer@example.com", "SecurePass123!")
    auth_store.reset_failed_attempts("test.engineer@example.com")

    # 4 failed attempts should fail normally
    for _ in range(4):
        with pytest.raises(ValueError) as exc:
            auth_store.login_user("test.engineer@example.com", "WrongPassword!")
        assert "Invalid email or password" in str(exc.value)

    # 5th failed attempt triggers lockout
    with pytest.raises(ValueError) as exc:
        auth_store.login_user("test.engineer@example.com", "WrongPassword!")
    assert "Invalid email or password" in str(exc.value)

    # 6th attempt is blocked by lockout
    with pytest.raises(ValueError) as exc:
        auth_store.login_user("test.engineer@example.com", "SecurePass123!")
    assert "locked" in str(exc.value).lower()
