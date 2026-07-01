from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"][0] == "michael@mergington.edu"


def test_signup_for_activity_adds_participant():
    email = "new.student@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for Chess Club"

    # Restore state for subsequent tests
    client.delete(f"/activities/Chess Club/participants/{email}")


def test_signup_rejects_duplicate_participant():
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert data["activity"] == "Chess Club"
    assert "michael@mergington.edu" not in data["participants"]

    # Restore the original state for later tests
    client.post("/activities/Chess Club/signup?email=michael@mergington.edu")


def test_unregister_missing_participant_returns_not_found():
    response = client.delete("/activities/Chess Club/participants/does-not-exist@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_unknown_activity_returns_not_found():
    response = client.post("/activities/Unknown Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
