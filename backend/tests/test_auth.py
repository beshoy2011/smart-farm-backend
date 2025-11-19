"""
Tests for authentication
"""

import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine, SessionLocal
from main import app

# Create test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture
def db_session():
    """Create a test database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_login():
    """Test user login"""
    # First register
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "testpass123"
        }
    )
    
    # Then login
    response = client.post(
        "/api/auth/login",
        data={
            "username": "loginuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    """Test getting current user"""
    # Register and login
    client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "testpass123"
        }
    )
    
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "meuser",
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"

