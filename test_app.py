import pytest
from app import app  
from database import initialize_database

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        initialize_database()  
        yield client

def test_predict_issue(client):
    """Test of endpoint /api/predict"""
    payload = {"title": "Bug in login", "body": "Unable to log in with correct credentials."}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    assert "label" in data
    assert "confidence" in data

def test_predict_empty_title(client):
    """Test of endpoint /api/predict with empty title"""
    payload = {"title": "", "body": "Test body"}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Title is empty"

def test_predict_empty_body(client):
    """Test of endpoint /api/predict with empty body"""
    payload = {"title": "test title", "body": ""}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Body is empty"

def test_correct_issue(client):
    """Test of endpoint /api/correct"""
    payload = {"title": "Bug in login", "body": "Unable to log in with correct credentials."}
    response = client.post("/api/predict", json=payload)
    issue_id = response.get_json()["id"]

    correction_payload = {"issue_id": issue_id, "corrected_label": "bug"}
    correction_response = client.post("/api/correct", json=correction_payload)
    assert correction_response.status_code == 200
    data = correction_response.get_json()
    assert data["id"] == issue_id
    assert data["corrected_label"] == "bug"

def test_correct_issue_not_found(client):
    """Test of endpoint /api/correct with invalid id"""
    payload = {"issue_id": "123", "corrected_label": "bug"}
    response = client.post("/api/correct", json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Issue ID not found"
