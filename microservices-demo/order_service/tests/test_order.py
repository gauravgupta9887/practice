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

def test_order(client):
    # create a product first
    prod_id = 1
    # ensure a user & token
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=1)

    # create order
    resp = client.post("/api/order/orders",
                       json={"product_id": prod_id, "quantity": 2},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["quantity"] == 2