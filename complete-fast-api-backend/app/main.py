import time
from random import randrange

import psycopg2
from app.database import get_db
from app.routers import auth, post, user, vote
from app.schemas import Post
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models

# from .database import engine
# This is not needed as we have done the creation already with alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Our actual main file is till here only and imports are also not needed
#
#
#
#
#
#
#
#

# made it obselete
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Db connection was successful")
        break
    except Exception as e:
        print("Db connection was not successful", e)
        time.sleep()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/create-post")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return f"new post: title:{payload['title']},content:{payload['content']}"


# title sr, content str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_new_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published)
                VALUES (%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()

    # this block is not getting executed anymore
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": new_post}


# title sr, content str


@app.get("/posts/latest")
def get_latest_post():
    return {"detail": my_posts[-1]}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts where id=%s""", (str(id),))
    test_post = cursor.fetchone()
    # post = find_post(id)
    if not test_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_detail": test_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s,content=%s, published=%s
                   WHERE id=%s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    # post_index = find_post_index(id)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[post_index] = post_dict
    return {"put_detail": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # post_index = find_post_index(id)
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    # my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
