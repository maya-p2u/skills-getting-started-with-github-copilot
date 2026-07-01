from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert data["activity"] == "Chess Club"
    assert "michael@mergington.edu" not in data["participants"]

    # Restore the original state for later tests
    client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
