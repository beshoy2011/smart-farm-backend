"""
Tests for analysis endpoints
"""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
from main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    """Get authentication token"""
    # Register
    client.post(
        "/api/auth/register",
        json={
            "email": "analysis@example.com",
            "username": "analysistest",
            "password": "testpass123"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        data={
            "username": "analysistest",
            "password": "testpass123"
        }
    )
    return response.json()["access_token"]


def create_test_image():
    """Create a test image"""
    img = Image.new('RGB', (224, 224), color='green')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


def test_analyze_image(auth_token):
    """Test image analysis"""
    img_buffer = create_test_image()
    
    response = client.post(
        "/api/analysis/analyze_image",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"file": ("test.jpg", img_buffer, "image/jpeg")},
        data={"plant_type": "tomato"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "plant_health_score" in data
    assert "water_needs" in data
    assert "recommendations" in data


def test_predict_water(auth_token):
    """Test water prediction"""
    response = client.get(
        "/api/analysis/predict_water",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={
            "plant_type": "tomato",
            "soil_moisture": 0.5,
            "temperature": 25.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "water_needs" in data
    assert isinstance(data["water_needs"], (int, float))


def test_get_analysis_history(auth_token):
    """Test getting analysis history"""
    response = client.get(
        "/api/analysis/history",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"skip": 0, "limit": 10}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

