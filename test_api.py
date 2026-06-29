from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_delete_vault():
    login = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "1234"
        }
    )

    token = login.json()["access_token"]

    response = client.delete(
        "/vault/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200 