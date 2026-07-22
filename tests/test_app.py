from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app import models
from app.auth import hash_password, verify_password

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200


def test_login_page():
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_dashboard_page():
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_protected_links_are_hidden_for_guests():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'data-nav="dashboard"' not in html
    assert 'data-nav="contribute"' not in html
    assert 'data-nav="review"' not in html
    assert 'data-nav="dataset"' not in html
    assert 'data-nav="profile"' not in html
    assert 'data-nav="admin"' not in html


def test_password_hashing_round_trip():
    password = "secure-password-123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)
