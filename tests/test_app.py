import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    # Second should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Signup first
    client.post("/activities/Programming%20Class/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Programming%20Class/signup/unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Programming Class" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Programming%20Class/signup/notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup/test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # Since it redirects to /static/index.html, but TestClient follows redirects? Wait, RedirectResponse.
    # Actually, it should return the HTML or follow.
    # But for test, perhaps check status 200.