import urllib.parse

import src.app as app_module


# Tests follow the Arrange-Act-Assert (AAA) pattern for clarity.

def test_get_activities_returns_expected_structure(client):
    # Arrange: none (server has in-memory activities)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity from the seed data
    assert "Chess Club" in data


def test_signup_success_updates_participants(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test_student@example.com"

    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity_name)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    # Use an existing participant from seed data
    existing = app_module.activities[activity_name]["participants"][0]

    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity_name)}/signup", params={"email": existing})

    # Assert
    assert resp.status_code == 400


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "someone@example.com"

    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity_name)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_delete_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    # pick existing participant
    email = app_module.activities[activity_name]["participants"][0]

    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity_name)}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@example.com"

    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity_name)}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_delete_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "No Such Activity"
    email = "someone@example.com"

    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity_name)}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
