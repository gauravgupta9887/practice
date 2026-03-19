import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/sqlalchemy/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_list = list(map(validate, res.json()))
    print(posts_list)
    assert len(res.json()) == 3
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/sqlalchemy/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/sqlalchemy/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_user_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/sqlalchemy/posts/890")

    assert res.status_code == 404


def test_user_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/sqlalchemy/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("title 1", "content 1", True),
        ("title 2", "content 2", True),
        ("title 3", "content 3", False),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/sqlalchemy/posts",
        json={"title": title, "content": content, "published": published},
    )
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/sqlalchemy/posts",
        json={"title": "title", "content": "content"},
    )
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/sqlalchemy/posts",
        json={"title": "title", "content": "content"},
    )

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/sqlalchemy/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/sqlalchemy/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/sqlalchemy/posts/900")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/sqlalchemy/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "title 30",
        "content": "content 30",
        "published": True,
    }
    res = authorized_client.put(f"/sqlalchemy/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    # print(updated_post)
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.published == data["published"]
