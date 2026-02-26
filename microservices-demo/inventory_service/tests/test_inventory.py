import pytest
from .app import create_app
from .shared.db import SessionLocal, Base, engine

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    client = app.test_client()
    yield client
    with app.app_context():
        Base.metadata.drop_all(bind=engine)

def test_create_product(client):
    # need a token – use user service to get one
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=1)

    resp = client.post("/api/inventory/products",
                       json={"name":"Widget","price":12.34,"quantity":5},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    prod = resp.get_json()
    assert prod["name"]=="Widget"

    # read
    resp = client.get(f"/api/inventory/products/{prod['id']}",
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"]=="Widget"