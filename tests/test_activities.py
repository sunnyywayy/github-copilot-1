import pytest
from fastapi import status

# Use the client fixture from conftest.py

def test_get_activities(client):
    # Arrange & Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_duplicate(client):
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_success(client):
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert f"Unregistered {email}" in response.json()["message"]


def test_unregister_not_registered(client):
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not registered" in response.json()["detail"]


def test_signup_activity_not_found(client):
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found(client):
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]
