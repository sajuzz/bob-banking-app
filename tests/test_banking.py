import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "BACKEND"))

from app import app as flask_app
from database import init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test_banking.db")
    import database
    monkeypatch.setattr(database, "DB_PATH", db_file)
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret"
    init_db()
    with flask_app.test_client() as client:
        yield client


# ── Auth tests ──────────────────────────────────────────────────────────────

def test_login_success(client):
    res = client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    assert res.status_code == 200
    assert res.get_json()["username"] == "alice"


def test_login_wrong_password(client):
    res = client.post("/api/auth/login", json={"username": "alice", "password": "wrong"})
    assert res.status_code == 401


def test_login_unknown_user(client):
    res = client.post("/api/auth/login", json={"username": "nobody", "password": "x"})
    assert res.status_code == 401


def test_login_missing_fields(client):
    res = client.post("/api/auth/login", json={"username": ""})
    assert res.status_code == 400


def test_logout(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/auth/logout")
    assert res.status_code == 200


# ── Account tests ────────────────────────────────────────────────────────────

def test_balance_requires_login(client):
    res = client.get("/api/account/balance")
    assert res.status_code == 401


def test_balance_after_login(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.get("/api/account/balance")
    assert res.status_code == 200
    assert "balance" in res.get_json()


def test_deposit(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/account/deposit", json={"amount": 100})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["balance"] == 5100.0


def test_deposit_zero(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/account/deposit", json={"amount": 0})
    assert res.status_code == 400


def test_withdraw(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/account/withdraw", json={"amount": 500})
    assert res.status_code == 200
    assert res.get_json()["balance"] == 4500.0


def test_withdraw_insufficient_funds(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/account/withdraw", json={"amount": 99999})
    assert res.status_code == 400
    assert "Insufficient" in res.get_json()["error"]


def test_withdraw_negative(client):
    client.post("/api/auth/login", json={"username": "alice", "password": "alice123"})
    res = client.post("/api/account/withdraw", json={"amount": -50})
    assert res.status_code == 400
