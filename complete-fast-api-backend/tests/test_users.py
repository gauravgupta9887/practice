import pytest
from app.schemas import Token, UserOut
from jose import jwt
from app.config import settings


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


@pytest.mark.parametrize(
    "email, password, status_code",
    [("abc@gmail.com", "pass", 403), (None, "pass", 422)],
)
def test_incorrect_login(
    client, session, test_user, email, password, status_code
):  # noqa
    res = client.post(
        "/login/",
        data={
            "username": email,
            "password": password,
        },  # noqa
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
