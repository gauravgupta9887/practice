from fastapi.testclient import TestClient
from app.config import settings
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models
import pytest
from app.schemas import Token, UserOut
from jose import jwt

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


def test_root(client, session):  # noqa
    res = client.get("/")
    print(res)
    print(res.json())
    print(res.json().get("message", ""))
    print(res.status_code)
    assert res.json().get("message", "") == "Hello World"


def test_create_user(client, session):  # noqa

    res = client.post("/users/", json={"email": "abcdef@gmail.com", "password": "123"})
    new_user = UserOut(**res.json())
    assert new_user.email == "abcdef@gmail.com"
    print(res.json())
    assert res.status_code == 201


def test_login_user(client, session, test_user):  # noqa
    res = client.post(
        "/login/",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },  # noqa
    )
    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
