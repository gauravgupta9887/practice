import pytest
from .app import create_app
from .shared.db import SessionLocal

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        # clean DB before each test
        SessionLocal().execute('DELETE FROM users')
        SessionLocal().commit()
    client = app.test_client()
    yield client
    # teardown: nothing required

def test_register_and_login(client):
    # register
    resp = client.post("/api/users/register",
                       json={"email":"alice@example.com","password":"secret"})
    assert resp.status_code == 201
    uid = resp.get_json()["id"]

    # login
    resp = client.post("/api/users/login",
                       json={"email":"alice@example.com","password":"secret"})
    assert resp.status_code == 200
    token = resp.get_json()["access_token"]
    assert token

    # profile
    resp = client.get("/api/users/profile",
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["email"] == "alice@example.com"