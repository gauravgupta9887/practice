from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# made it obselete
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Db connection was successful")
        break
    except Exception as e:
        print("Db connection was not successful", e)
        time.sleep()

my_posts = [{"title": "title of post 1", "content": "content of post 1",
            "id": 1}, {"title": "favorite foods", "content": "I like pizza",
            "id": 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/sqlalchemy/posts")
async def get_sqlalchemy_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/create-post")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return (f"new post: title:{payload['title']},content:{payload['content']}")
# title sr, content str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_new_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content,
                                                    post.published))
    new_post = cursor.fetchone()
    conn.commit()

    # this block is not getting executed anymore
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": new_post}
# title sr, content str


@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED)
def create_new_sqlalchemy_post(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    post_dict = post.dict()
    del post_dict['rating']
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # this block is not getting executed anymore
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": test_post}


@app.get("/sqlalchemy/posts/{id}")
def get_sqlalchemy_post(id: int, db: Session = Depends(get_db)):
    test_post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts where id=%s""", (str(id),))
    # test_post = cursor.fetchone()
    # post = find_post(id)
    print(test_post)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": test_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # post_index = find_post_index(id)
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",
                   (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/sqlalchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sqlalchemy_post(id: int, db: Session = Depends(get_db)):
    # post_index = find_post_index(id)
    deleted_query = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # my_posts.pop(post_index)
    deleted_query.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s, published=%s
                   WHERE id=%s RETURNING *""", (post.title, post.content,
                                                post.published, str(id)))
    # post_index = find_post_index(id)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[post_index] = post_dict
    return {"put_detail": updated_post}
