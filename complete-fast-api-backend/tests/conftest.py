from fastapi.testclient import TestClient
from app.config import settings
from app.oauth2 import create_access_token
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models
import pytest

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/
# hostname>/<database_name'
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/"
    f"{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    # run our code before we run our test
    print("my session fixture ran")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):  # noqa
    user_data = {"email": "abcdef@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_1(client):  # noqa
    user_data = {"email": "abcdefgh@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, session, test_user_1):
    posts_data = [
        {
            "title": "title 1",
            "content": "content 1",
            "user_id": test_user["id"],
        },
        {
            "title": "title 2",
            "content": "content 2",
            "user_id": test_user["id"],
        },
        {
            "title": "title 3",
            "content": "content 3",
            "user_id": test_user["id"],
        },
        {
            "title": "title 4",
            "content": "content 4",
            "user_id": test_user_1["id"],
        },
    ]

    session.add_all(list(map(lambda x: models.Post(**x), posts_data)))
    session.commit()

    return session.query(models.Post).all()
