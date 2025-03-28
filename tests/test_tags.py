import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database import get_db
from models import Tag
from schemas import TagCreate

client = TestClient(app)

# Dependency override for testing
def override_get_db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def setup_function():
    # Clear the tags table before each test
    db = next(get_db())
    db.query(Tag).delete()
    db.commit()

def test_add_tag():
    response = client.post("/tags/", json={"name": "Test Tag"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tag"

def test_add_tag_invalid():
    response = client.post("/tags/", json={})  # Missing required fields
    assert response.status_code == 422

def test_list_tags():
    response = client.get("/tags/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tag():
    response = client.post("/tags/", json={"name": "Another Tag"})
    tag_id = response.json()["id"]
    response = client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Another Tag"

def test_get_tag_not_found():
    response = client.get("/tags/999")  # Non-existent tag ID
    assert response.status_code == 404

def test_update_tag():
    response = client.post("/tags/", json={"name": "Tag to Update"})
    tag_id = response.json()["id"]
    response = client.put(f"/tags/{tag_id}", json={"name": "Updated Tag"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Tag"

def test_update_tag_not_found():
    response = client.put("/tags/999", json={"name": "Non-existent Tag"})
    assert response.status_code == 404

def test_delete_tag():
    response = client.post("/tags/", json={"name": "Tag to Delete"})
    tag_id = response.json()["id"]
    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Tag deleted successfully"

def test_delete_tag_not_found():
    response = client.delete("/tags/999")  # Non-existent tag ID
    assert response.status_code == 404
