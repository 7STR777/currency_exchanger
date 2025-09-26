import pytest

def test_user_registration(client):
    user = {"username":"user1",
            "password":"testpass"}
    response = client.post("/auth/register", json=user)
    assert response.status_code == 200